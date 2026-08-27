# NetSage AI
# AI-Assisted Network Troubleshooting Assistant

NetSage AI is an AI-assisted network troubleshooting application that combines deterministic network checks with Gemini-based diagnostic reasoning.

The system analyzes predefined network troubleshooting cases, examines network command output, runs deterministic checks, generates a structured AI diagnosis, presents the diagnosis to a human reviewer, and records the review decision in an audit log.

1. Project Objective

The objective of NetSage AI is to assist network engineers with troubleshooting by combining:

- Network evidence
- Deterministic rule-based checks
- AI-assisted diagnosis
- Human review
- Audit logging

The AI does not directly make configuration changes.

Instead, it produces a proposed diagnosis and recommended next steps that must be reviewed by a human operator.

2. Main Workflow

The application follows this workflow:

Case Selection
      |
      v
Load Case from cases.csv
      |
      v
Network Evidence
      |
      v
Deterministic Rule Checker
      |
      v
Evidence-Grounded Gemini Diagnosis
      |
      v
Structured JSON Validation
      |
      v
Streamlit Interface
      |
      v
Human Review
   +--+----+
   |  |    |
   v  v    v
Approve Edit Reject
   +--+----+
      |
      v
Audit Log

3. Project Structure

NetSage-AI/
|
+-- .env
+-- .gitignore
+-- README.md
+-- pytest.ini
|
+-- data/
|   +-- cases.csv
|
+-- docs/
|   +-- model_audit_log.md
|
+-- prompts/
|   +-- diagnose_prompt.md
|
+-- src/
|   +-- __init__.py
|   +-- app.py
|   +-- checker.py
|   +-- engine.py
|   +-- test_gemini.py
|
+-- tests/
|   +-- test_checker.py
|
+-- venv/

4. Technologies Used

The project uses:

- Python
- Streamlit
- Pandas
- Python-dotenv
- Google GenAI SDK
- Gemini API
- Pytest
- CSV-based case data
- Markdown audit logging

5. Environment Setup

Create a virtual environment

Windows PowerShell:

python -m venv venv

Activate it:

.\venv\Scripts\Activate.ps1

If PowerShell execution policy prevents activation, use:

venv\Scripts\activate.bat

6. Install Dependencies

Install the required packages:

pip install streamlit pandas python-dotenv pytest google-genai


7. Gemini API Configuration

Create a .env file in the project root:

GEMINI_API_KEY=YOUR_API_KEY

Do not commit the API key to Git.

The .env file should be included in .gitignore.

8. Run the Application

From the project root:

python -m streamlit run src/app.py

Streamlit will provide a local address, normally:

http://localhost:8501

Streamlit-Deployed-Link - https://netsage-ai-manas.streamlit.app/

Open that address in your browser.

9. Using NetSage AI

Step 1 - Select a Case

Enter a case ID such as:

NET-001

Step 2 - Run Diagnosis

Click:

Run Diagnosis

The application loads the case and sends the relevant evidence through the troubleshooting pipeline.

Step 3 - Review the AI Diagnosis

The application displays:

- Root cause
- OSI layer
- Confidence
- Evidence
- Recommended next command
- Proposed fix steps

Step 4 - Human Review

The reviewer can:

- Approve
- Edit
- Reject

Step 5 - Audit Logging

The human decision is recorded in:

docs/model_audit_log.md

10. Deterministic Checker

The deterministic checker analyzes network command output before the AI diagnosis.

This provides a layer of evidence-based analysis before the information is passed to Gemini.

The checker is implemented in:

src/checker.py

The checker is tested using:

tests/test_checker.py

11. AI Diagnosis

The AI diagnosis is implemented in:

src/engine.py

Gemini receives:

- Case information
- Network output
- Deterministic checker findings

The AI is instructed to remain grounded in the supplied evidence.

The expected response structure is:

{
    "root_cause": "string",
    "osi_layer": "string",
    "confidence": 0.0,
    "evidence": [],
    "next_command": "string",
    "fix_steps": []
}

The Python application validates the returned structure before displaying it.

12. Evidence Grounding

NetSage AI instructs the model not to invent network evidence.

The model should not invent:

- Interfaces
- IP addresses
- VLANs
- Routes
- Protocols
- Device states
- Error messages
- Topology relationships
- Commands that were supposedly executed

Evidence shown in the diagnosis should come from the supplied case data or deterministic checker results.

13. Human-in-the-Loop

The AI diagnosis is a proposal rather than an automatic configuration change.

A human reviewer must review the diagnosis.

Possible decisions are:

APPROVED
EDITED
REJECTED

This prevents the AI from directly modifying network devices.

14. Audit Logging

Review decisions are stored in:

docs/model_audit_log.md

An audit entry records information such as:

- Case ID
- AI root cause
- OSI layer
- Confidence
- Evidence
- Recommended command
- Proposed fix steps
- Human decision
- Human comment

15. Running Tests

Run the automated tests with:

pytest

The current checker test suite should complete successfully.

16. Testing the Gemini Connection

A development test is available at:

src/test_gemini.py

Run it with:

python src/test_gemini.py

This verifies that the Gemini API connection is available.

17. Testing the Engine

The engine can also be tested directly:

python src/engine.py

The test uses:

NET-001

and prints the generated diagnosis.

 18. Security

Never commit:

.env

to a public repository.

The API key should remain in the environment configuration.

The .gitignore file should contain:

.env
venv/
__pycache__/
*.pyc

19. Current Limitations

The current prototype uses predefined troubleshooting cases stored in:

data/cases.csv

It does not directly connect to live production network devices.

The AI generates proposed diagnostic commands and remediation steps but does not automatically execute configuration changes.

Human review is required before accepting a diagnosis.

20. Future Enhancements

Possible future improvements include:

- Live Cisco device integration
- SSH-based evidence collection
- Larger troubleshooting datasets
- More deterministic network checks
- More advanced structured AI output
- Role-based access control
- Database-backed audit logs
- Authentication
- Dashboard analytics
- Historical incident analysis
- Automated regression evaluation
- Production deployment



21. Safety Principle

NetSage AI follows a human-in-the-loop design.

The AI proposes:

Diagnosis
Evidence
Next diagnostic command
Proposed remediation

A human operator decides whether the recommendation should be accepted.

The system does not automatically make network configuration changes.


22. Quick Start

After cloning or opening the project:

cd NetSage-AI

Activate the virtual environment.

Install dependencies:

pip install streamlit pandas python-dotenv pytest google-genai

Configure:

.env

with:

GEMINI_API_KEY=YOUR_API_KEY

Run tests:

pytest

Start the application:

python -m streamlit run src/app.py

Open the Streamlit URL in the browser.

Enter:

NET-001

and click:

Run Diagnosis

23. Project Status

Current implementation includes:

- Case-based troubleshooting
- Deterministic network checks
- Gemini-assisted diagnosis
- Evidence-grounded prompting
- Structured diagnosis validation
- Streamlit interface
- Human approval
- Human editing
- Human rejection
- Audit logging
- Automated checker tests


24. License

This project is currently intended as an educational/prototype project.

