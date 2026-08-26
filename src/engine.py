import csv
import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from google import genai

# ---------------------------------------------------------
# Import checker
# ---------------------------------------------------------
# This works both when running:
#     python src/engine.py
# and when importing:
#     from src.engine import diagnose
#
try:
    from .checker import check_output
except ImportError:
    from checker import check_output


# =========================================================
# PATHS
# =========================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = ROOT_DIR / "data"
DOCS_DIR = ROOT_DIR / "docs"

CASES_FILE = DATA_DIR / "cases.csv"
AUDIT_LOG_FILE = DOCS_DIR / "model_audit_log.md"


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv(ROOT_DIR / ".env")


# =========================================================
# GEMINI CONFIGURATION
# =========================================================

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY was not found. "
        "Make sure it exists in the .env file."
    )


client = genai.Client(
    api_key=API_KEY
)


MODEL_NAME = "gemini-3.5-flash-lite"


# =========================================================
# LOAD CASES
# =========================================================

def load_cases() -> list[dict[str, Any]]:
    """
    Load all troubleshooting cases from data/cases.csv.
    """

    if not CASES_FILE.exists():
        raise FileNotFoundError(
            f"Cases file not found: {CASES_FILE}"
        )

    with open(
        CASES_FILE,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        cases = list(reader)

    if not cases:
        raise ValueError(
            "cases.csv does not contain any cases."
        )

    return cases


# =========================================================
# FIND CASE
# =========================================================

def get_case(case_id: str) -> dict[str, Any]:
    """
    Find one troubleshooting case by Case ID.
    """

    cases = load_cases()

    requested_id = case_id.strip().upper()

    for case in cases:

        current_id = str(
            case.get("case_id", "")
        ).strip().upper()

        if current_id == requested_id:
            return case

    available_ids = [
        str(case.get("case_id", ""))
        for case in cases
    ]

    raise ValueError(
        f"Case '{case_id}' was not found. "
        f"Available cases: {available_ids}"
    )


# =========================================================
# CONVERT CSV VALUES
# =========================================================

def parse_possible_json(value: Any) -> Any:
    """
    Some CSV fields may contain JSON-like data.
    Convert them when possible; otherwise return the
    original value.
    """

    if value is None:
        return None

    if not isinstance(value, str):
        return value

    text = value.strip()

    if not text:
        return ""

    try:
        return json.loads(text)

    except (json.JSONDecodeError, TypeError):
        return value


# =========================================================
# GET SHOW OUTPUT
# =========================================================

def get_show_output(case: dict[str, Any]) -> str:
    """
    Extract network command output from the case.

    The function supports the expected show_outputs field
    and also falls back to common alternative field names.
    """

    possible_fields = [
        "show_outputs",
        "show_output",
        "evidence",
        "network_output",
        "command_output"
    ]

    for field in possible_fields:

        value = case.get(field)

        if value is not None and str(value).strip():

            parsed = parse_possible_json(value)

            if isinstance(parsed, (dict, list)):
                return json.dumps(
                    parsed,
                    indent=2,
                    ensure_ascii=False
                )

            return str(parsed)

    return ""


# =========================================================
# BUILD DIAGNOSTIC INPUT
# =========================================================

def build_diagnostic_input(
    case: dict[str, Any],
    checker_result: Any
) -> dict[str, Any]:
    """
    Build the exact information that will be supplied
    to Gemini.

    This keeps the model grounded in the actual case
    and deterministic checker output.
    """

    diagnostic_input = {
        "case_id": case.get("case_id"),
        "severity": case.get("severity"),
        "symptom": case.get("symptom"),
        "topology_note": case.get("topology_note"),
        "expected_osi_layer": case.get("osi_layer"),
        "expected_fault": case.get("expected_fault"),
        "show_outputs": get_show_output(case),
        "checker_result": checker_result
    }

    return diagnostic_input


# =========================================================
# BUILD GEMINI PROMPT
# =========================================================

def build_prompt(
    diagnostic_input: dict[str, Any]
) -> str:
    """
    Build the evidence-grounded Gemini prompt.
    """

    return f"""
You are the diagnostic reasoning component of NetSage AI,
an AI-assisted network troubleshooting system.

Your task is to analyze ONLY the network information supplied
below and produce a proposed diagnosis.

============================================================
NETWORK CASE DATA
============================================================

{json.dumps(
    diagnostic_input,
    indent=2,
    ensure_ascii=False
)}

============================================================
EVIDENCE-GROUNDING RULES
============================================================

1. Use ONLY the information provided in NETWORK CASE DATA.

2. Do NOT invent:
   - interfaces
   - IP addresses
   - VLANs
   - routes
   - protocols
   - configuration commands
   - topology relationships
   - device states
   - error messages
   - network failures

3. The "evidence" field must contain evidence that is directly
   supported by the supplied case data or checker result.

4. Do NOT use general networking knowledge as evidence.

5. General networking knowledge may be used to explain WHY
   the supplied evidence indicates a particular fault, but it
   must not be presented as observed evidence.

6. If the supplied evidence is insufficient to determine the
   root cause with high confidence, explicitly say that the
   evidence is insufficient.

7. Do not assume that the expected_fault field is automatically
   correct. Evaluate the actual evidence.

8. Deterministic checker findings should be treated as strong
   evidence when they directly correspond to the supplied
   network output.

9. The recommended next command must be relevant to the case
   and must NOT claim that the command has already been executed.

10. Fix steps are proposed actions only. Do NOT claim that the
    configuration has already been changed.

11. Do not claim that a network device was successfully repaired.

12. Do not claim that a command was executed unless the supplied
    case data explicitly says that it was executed.

============================================================
CONFIDENCE RULES
============================================================

Confidence must be a number between 0 and 1.

Use approximately:

0.90 - 1.00
Direct evidence strongly identifies the fault.

0.70 - 0.89
Evidence strongly suggests the fault but additional
verification is useful.

0.50 - 0.69
There are indications of the fault but significant
uncertainty remains.

Below 0.50
Evidence is insufficient for a reliable diagnosis.

Do not use 0.95 or higher simply because the diagnosis sounds
plausible.

High confidence requires strong, direct evidence.

============================================================
OUTPUT FORMAT
============================================================

Return ONLY valid JSON.

Do not return Markdown.

Do not use ```json.

Do not return explanations outside the JSON.

Use exactly this structure:

{{
    "root_cause": "string",
    "osi_layer": "string",
    "confidence": 0.0,
    "evidence": [
        "string"
    ],
    "next_command": "string",
    "fix_steps": [
        "string"
    ]
}}

============================================================
FIELD REQUIREMENTS
============================================================

root_cause:
Explain the most likely network fault based on the supplied
evidence.

osi_layer:
Identify the relevant OSI layer.

confidence:
A number from 0 to 1.

evidence:
List ONLY evidence actually present in the supplied network
case or checker result.

next_command:
Provide ONE useful command that would help verify or
investigate the diagnosis.

fix_steps:
Provide practical proposed remediation steps.

Remember:

OBSERVED EVIDENCE != GENERAL NETWORK KNOWLEDGE

Only observed or supplied information may appear in the
evidence field.
"""


# =========================================================
# CLEAN GEMINI RESPONSE
# =========================================================

def clean_json_response(
    response_text: str
) -> str:
    """
    Remove accidental Markdown code fences from Gemini's
    response.
    """

    text = response_text.strip()

    if text.startswith("```json"):
        text = text[7:]

    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    return text.strip()


# =========================================================
# VALIDATE DIAGNOSIS
# =========================================================

def validate_diagnosis(
    diagnosis: Any
) -> dict[str, Any]:
    """
    Validate the basic structure of the Gemini diagnosis.

    This is an important safety layer between Gemini and
    the Streamlit application.
    """

    if not isinstance(diagnosis, dict):
        raise ValueError(
            "Gemini response is not a JSON object."
        )

    required_fields = [
        "root_cause",
        "osi_layer",
        "confidence",
        "evidence",
        "next_command",
        "fix_steps"
    ]

    missing_fields = [
        field
        for field in required_fields
        if field not in diagnosis
    ]

    if missing_fields:

        raise ValueError(
            "Gemini diagnosis is missing required fields: "
            + ", ".join(missing_fields)
        )

    # -----------------------------------------------------
    # Validate root cause
    # -----------------------------------------------------

    if not isinstance(
        diagnosis["root_cause"],
        str
    ):

        raise ValueError(
            "root_cause must be a string."
        )

    # -----------------------------------------------------
    # Validate OSI layer
    # -----------------------------------------------------

    if not isinstance(
        diagnosis["osi_layer"],
        str
    ):

        raise ValueError(
            "osi_layer must be a string."
        )

    # -----------------------------------------------------
    # Validate confidence
    # -----------------------------------------------------

    try:

        confidence = float(
            diagnosis["confidence"]
        )

    except (
        TypeError,
        ValueError
    ):

        raise ValueError(
            "confidence must be a number."
        )

    if not 0 <= confidence <= 1:

        raise ValueError(
            "confidence must be between 0 and 1."
        )

    diagnosis["confidence"] = confidence

    # -----------------------------------------------------
    # Validate evidence
    # -----------------------------------------------------

    if not isinstance(
        diagnosis["evidence"],
        list
    ):

        raise ValueError(
            "evidence must be a list."
        )

    diagnosis["evidence"] = [
        str(item)
        for item in diagnosis["evidence"]
    ]

    # -----------------------------------------------------
    # Validate next command
    # -----------------------------------------------------

    if not isinstance(
        diagnosis["next_command"],
        str
    ):

        raise ValueError(
            "next_command must be a string."
        )

    # -----------------------------------------------------
    # Validate fix steps
    # -----------------------------------------------------

    if not isinstance(
        diagnosis["fix_steps"],
        list
    ):

        raise ValueError(
            "fix_steps must be a list."
        )

    diagnosis["fix_steps"] = [
        str(step)
        for step in diagnosis["fix_steps"]
    ]

    return diagnosis


# =========================================================
# GENERATE GEMINI DIAGNOSIS
# =========================================================

def generate_gemini_diagnosis(
    diagnostic_input: dict[str, Any]
) -> dict[str, Any]:
    """
    Send the grounded diagnostic input to Gemini and
    return a validated structured diagnosis.
    """

    prompt = build_prompt(
        diagnostic_input
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    response_text = getattr(
        response,
        "text",
        None
    )

    if not response_text:

        raise RuntimeError(
            "Gemini returned an empty response."
        )

    cleaned_response = clean_json_response(
        response_text
    )

    try:

        diagnosis = json.loads(
            cleaned_response
        )

    except json.JSONDecodeError as error:

        raise ValueError(
            "Gemini returned invalid JSON.\n\n"
            f"Raw response:\n{response_text}"
        ) from error

    return validate_diagnosis(
        diagnosis
    )


# =========================================================
# MAIN DIAGNOSIS FUNCTION
# =========================================================

def diagnose(
    case_id: str
) -> dict[str, Any]:
    """
    Complete NetSage diagnosis pipeline.

    Flow:

        Case ID
          ↓
        cases.csv
          ↓
        checker.py
          ↓
        evidence-grounded Gemini
          ↓
        validated diagnosis
    """

    # -----------------------------------------------------
    # Load case
    # -----------------------------------------------------

    case = get_case(
        case_id
    )

    # -----------------------------------------------------
    # Extract show output
    # -----------------------------------------------------

    show_output = get_show_output(
        case
    )

    if not show_output:

        raise ValueError(
            f"No network show output found for case "
            f"{case_id}."
        )

    # -----------------------------------------------------
    # Run deterministic checker
    # -----------------------------------------------------

    checker_result = check_output(
        show_output
    )

    # -----------------------------------------------------
    # Build AI input
    # -----------------------------------------------------

    diagnostic_input = build_diagnostic_input(
        case,
        checker_result
    )

    # -----------------------------------------------------
    # Generate Gemini diagnosis
    # -----------------------------------------------------

    diagnosis = generate_gemini_diagnosis(
        diagnostic_input
    )

    # -----------------------------------------------------
    # Return complete result
    # -----------------------------------------------------

    return {
        "case": case,
        "checker_result": checker_result,
        "diagnostic_input": diagnostic_input,
        "diagnosis": diagnosis
    }


# =========================================================
# AUDIT LOG
# =========================================================

def save_audit_log(
    case_id: str,
    diagnosis: dict[str, Any],
    human_decision: str,
    human_comment: str = ""
) -> None:
    """
    Save the AI diagnosis and human decision to the
    model audit log.
    """

    DOCS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    AUDIT_LOG_FILE.touch(
        exist_ok=True
    )

    decision = str(
        human_decision
    ).upper()

    with open(
        AUDIT_LOG_FILE,
        "a",
        encoding="utf-8"
    ) as file:

        file.write("\n")
        file.write("---\n\n")

        file.write(
            f"## Case ID: {case_id}\n\n"
        )

        file.write(
            "### AI Diagnosis\n\n"
        )

        file.write(
            f"**Root Cause:** "
            f"{diagnosis.get('root_cause', '')}\n\n"
        )

        file.write(
            f"**OSI Layer:** "
            f"{diagnosis.get('osi_layer', '')}\n\n"
        )

        file.write(
            f"**Confidence:** "
            f"{diagnosis.get('confidence', '')}\n\n"
        )

        file.write(
            "### Evidence\n\n"
        )

        evidence = diagnosis.get(
            "evidence",
            []
        )

        for item in evidence:

            file.write(
                f"- {item}\n"
            )

        file.write("\n")

        file.write(
            "### Recommended Next Command\n\n"
        )

        file.write(
            "```text\n"
        )

        file.write(
            str(
                diagnosis.get(
                    "next_command",
                    ""
                )
            )
        )

        file.write(
            "\n```\n\n"
        )

        file.write(
            "### Proposed Fix Steps\n\n"
        )

        fix_steps = diagnosis.get(
            "fix_steps",
            []
        )

        for index, step in enumerate(
            fix_steps,
            start=1
        ):

            file.write(
                f"{index}. {step}\n"
            )

        file.write("\n")

        file.write(
            "### Human Review\n\n"
        )

        file.write(
            f"**Decision:** {decision}\n\n"
        )

        file.write(
            f"**Comment:** {human_comment}\n\n"
        )


# =========================================================
# COMMAND-LINE TEST
# =========================================================

if __name__ == "__main__":

    print(
        "=============================================="
    )

    print(
        "NetSage AI Engine Test"
    )

    print(
        "=============================================="
    )

    test_case_id = "NET-001"

    print(
        f"\nTesting case: {test_case_id}\n"
    )

    try:

        result = diagnose(
            test_case_id
        )

        print(
            "\nAI DIAGNOSIS:\n"
        )

        print(
            json.dumps(
                result["diagnosis"],
                indent=4,
                ensure_ascii=False
            )
        )

        print(
            "\n=============================================="
        )

        print(
            "Diagnosis generated successfully."
        )

        print(
            "=============================================="
        )

    except Exception as error:

        print(
            "\nERROR:"
        )

        print(
            str(error)
        )