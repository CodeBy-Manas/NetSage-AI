import streamlit as st
import pandas as pd

from src.engine import diagnose, save_audit_log


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="NetSage AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# GLOBAL CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       GLOBAL
       ===================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 75% 5%,
                rgba(54, 92, 180, 0.12),
                transparent 30%
            ),
            #070b13;
        color: #e7edf7;
    }

    .main .block-container {
        max-width: 1500px;
        padding-top: 1.4rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
        padding-bottom: 2rem;
    }

    /* =====================================================
       SIDEBAR
       ===================================================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #0b111d 0%,
                #080d16 100%
            );
        border-right: 1px solid #182234;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.2rem;
    }

    .brand {
        font-size: 24px;
        font-weight: 700;
        color: #f3f7ff;
        margin-bottom: 4px;
    }

    .brand-subtitle {
        color: #8995a8;
        font-size: 13px;
        line-height: 1.6;
        margin-bottom: 18px;
    }

    .sidebar-section {
        color: #707d91;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.08em;
        margin-top: 18px;
        margin-bottom: 8px;
    }

    .pipeline-item {
        padding: 9px 10px;
        border-radius: 8px;
        color: #aeb9c9;
        font-size: 13px;
        margin: 3px 0;
    }

    .pipeline-active {
        background: #15346e;
        color: #ffffff;
    }

    .warning-box {
        margin-top: 25px;
        padding: 14px;
        border-radius: 10px;
        background: #171432;
        border: 1px solid #2c285b;
        color: #b7b1e8;
        font-size: 12px;
        line-height: 1.6;
    }

    /* =====================================================
       HEADER
       ===================================================== */

    .page-title {
        font-size: 31px;
        font-weight: 700;
        color: #f5f7fb;
        margin-bottom: 2px;
    }

    .page-title span {
        color: #8c9cff;
    }

    .page-subtitle {
        color: #8c98aa;
        font-size: 13px;
        margin-bottom: 5px;
    }

    .page-description {
        color: #b2bccb;
        font-size: 12px;
        margin-bottom: 18px;
    }

    /* =====================================================
       PANELS
       ===================================================== */

    .panel {
        background:
            linear-gradient(
                145deg,
                rgba(19, 27, 43, 0.96),
                rgba(10, 16, 27, 0.96)
            );
        border: 1px solid #1c2940;
        border-radius: 10px;
        padding: 17px;
        margin-bottom: 10px;
        box-shadow:
            0 10px 25px rgba(0, 0, 0, 0.15);
    }

    .panel-title {
        font-size: 15px;
        font-weight: 650;
        color: #eef3fb;
        margin-bottom: 12px;
    }

    .panel-line {
        height: 1px;
        background: #1c2839;
        margin: 10px 0 14px 0;
    }

    /* =====================================================
       STATUS
       ===================================================== */

    .connected {
        display: inline-block;
        background: #09281f;
        color: #45dc9d;
        border: 1px solid #14543f;
        border-radius: 20px;
        padding: 5px 10px;
        font-size: 11px;
        font-weight: 600;
    }

    .success-box {
        background: #092c22;
        border: 1px solid #14573f;
        color: #65dfa8;
        border-radius: 7px;
        padding: 9px 12px;
        font-size: 12px;
        margin-top: 10px;
    }

    .pending-box {
        background: #34280d;
        border: 1px solid #725516;
        color: #e6c46b;
        border-radius: 7px;
        padding: 11px 13px;
        font-size: 12px;
    }

    /* =====================================================
       METRICS
       ===================================================== */

    .metric-card {
        min-height: 82px;
        padding: 13px 15px;
        border-right: 1px solid #202d40;
    }

    .metric-label {
        color: #7e8a9d;
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .metric-value {
        color: #f1f5fb;
        font-size: 20px;
        font-weight: 650;
        margin-top: 8px;
    }

    .severity-high {
        color: #ff7272;
    }

    .confidence-good {
        color: #52dfa0;
    }

    /* =====================================================
       SYMPTOM
       ===================================================== */

    .symptom-box {
        background: #142449;
        border: 1px solid #1e4380;
        border-radius: 7px;
        padding: 10px 12px;
        color: #77b5ff;
        font-size: 12px;
    }

    /* =====================================================
       TOPOLOGY
       ===================================================== */

    .topology-text {
        color: #b4bfce;
        font-size: 12px;
        margin-bottom: 10px;
    }

    /* =====================================================
       ROOT CAUSE
       ===================================================== */

    .root-cause {
        background:
            linear-gradient(
                135deg,
                rgba(87, 28, 39, 0.75),
                rgba(45, 20, 30, 0.85)
            );
        border: 1px solid #6b2b3a;
        border-radius: 8px;
        padding: 14px;
    }

    .root-title {
        color: #ff7070;
        font-weight: 650;
        font-size: 13px;
        margin-bottom: 6px;
    }

    .root-text {
        color: #ff9a9a;
        font-size: 12px;
        line-height: 1.55;
    }

    /* =====================================================
       EVIDENCE
       ===================================================== */

    .evidence-item {
        color: #b9c3d1;
        font-size: 11px;
        line-height: 1.5;
        margin-bottom: 8px;
    }

    /* =====================================================
       COMMAND
       ===================================================== */

    .command-box {
        background: #090f19;
        border: 1px solid #26354c;
        border-radius: 7px;
        padding: 11px 13px;
        color: #d8e2f2;
        font-family: Consolas, monospace;
        font-size: 11px;
    }

    /* =====================================================
       FIX STEPS
       ===================================================== */

    .fix-step {
        background: #101927;
        border: 1px solid #233148;
        border-radius: 8px;
        padding: 12px;
        color: #bfc9d7;
        font-size: 11px;
        min-height: 55px;
    }

    .step-number {
        display: inline-block;
        background: #1b56a7;
        color: white;
        width: 22px;
        height: 22px;
        text-align: center;
        line-height: 22px;
        border-radius: 50%;
        margin-right: 7px;
        font-weight: 600;
    }

    /* =====================================================
       STREAMLIT INPUTS
       ===================================================== */

    div[data-baseweb="select"] > div {
        background-color: #101722 !important;
        border-color: #26354a !important;
        color: #e5ebf4 !important;
    }

    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea {
        background-color: #101722 !important;
        border-color: #26354a !important;
        color: #e5ebf4 !important;
    }

    /* =====================================================
       BUTTONS
       ===================================================== */

    .stButton > button {
        border-radius: 7px;
        border: 1px solid #2b3b54;
        background: #111a29;
        color: #e4eaf3;
        font-size: 12px;
        min-height: 38px;
    }

    .stButton > button:hover {
        border-color: #5775c7;
        color: #ffffff;
    }

    /* =====================================================
       HIDE STREAMLIT DEFAULT UI
       ===================================================== */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SESSION STATE
# =========================================================

if "diagnosis_result" not in st.session_state:
    st.session_state.diagnosis_result = None

if "selected_case" not in st.session_state:
    st.session_state.selected_case = "NET-001"

if "review_status" not in st.session_state:
    st.session_state.review_status = "PENDING"

if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False


# =========================================================
# LOAD CASE DATA
# =========================================================

@st.cache_data
def load_cases():
    return pd.read_csv("data/cases.csv")


try:
    cases_df = load_cases()
except Exception as error:
    cases_df = None
    st.error("Unable to load data/cases.csv")
    st.exception(error)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="brand">◈ NetSage AI</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="brand-subtitle">'
        'AI-Assisted Network<br>'
        'Troubleshooting'
        '</div>',
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown(
        '<div class="sidebar-section">SYSTEM PIPELINE</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="pipeline-item pipeline-active">'
        '▣ &nbsp; 1. Case Selection'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="pipeline-item">'
        '◈ &nbsp; 2. Evidence Analysis'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="pipeline-item">'
        '◉ &nbsp; 3. Deterministic Checks'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="pipeline-item">'
        '✦ &nbsp; 4. Gemini Diagnosis'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="pipeline-item">'
        '♙ &nbsp; 5. Human Review'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="pipeline-item">'
        '▣ &nbsp; 6. Audit Logs'
        '</div>',
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown(
        '<div class="warning-box">'
        '<b>✦ AI recommendations may contain mistakes.</b>'
        '<br><br>'
        'Validate and review recommendations before acceptance.'
        '</div>',
        unsafe_allow_html=True,
    )


# =========================================================
# HEADER
# =========================================================

header_left, header_right = st.columns([7, 2])

with header_left:

    st.markdown(
        '<div class="page-title">'
        'NetSage AI <span>✦</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-subtitle">'
        'AI-Assisted Network Troubleshooting Assistant'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-description">'
        'Analyze network troubleshooting cases using '
        'deterministic checks and Gemini-assisted diagnosis.'
        '</div>',
        unsafe_allow_html=True,
    )


with header_right:

    st.markdown(
        '<div style="text-align:right;">'
        '<span class="connected">● CONNECTED</span>'
        '</div>',
        unsafe_allow_html=True,
    )


# =========================================================
# CASE SELECTION
# =========================================================

selection_col, overview_col = st.columns(
    [1.7, 1.25],
    gap="small",
)


with selection_col:

    st.markdown(
        '<div class="panel">',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="panel-title">'
        '📁 &nbsp; Case Selection'
        '</div>',
        unsafe_allow_html=True,
    )

    if cases_df is not None:

        case_options = cases_df["case_id"].astype(str).tolist()

        selected_case = st.selectbox(
            "Select Case",
            case_options,
            index=(
                case_options.index(
                    st.session_state.selected_case
                )
                if st.session_state.selected_case in case_options
                else 0
            ),
            format_func=lambda x: (
                f"{x} — "
                + str(
                    cases_df.loc[
                        cases_df["case_id"].astype(str) == x,
                        "title"
                    ].iloc[0]
                )
                if "title" in cases_df.columns
                else x
            ),
        )

        st.session_state.selected_case = selected_case

    else:

        selected_case = "NET-001"

    run_button = st.button(
        "▶  Run Diagnosis",
        type="primary",
        use_container_width=True,
    )

    if (
        st.session_state.diagnosis_result
        and not run_button
    ):

        st.markdown(
            '<div class="success-box">'
            '✓ &nbsp; Diagnosis prepared successfully.'
            '</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '</div>',
        unsafe_allow_html=True,
    )


# =========================================================
# CASE DATA HELPER
# =========================================================

def get_case_from_result(result):

    if not result:
        return {}

    return result.get("case", {})


# =========================================================
# RUN DIAGNOSIS
# =========================================================

if run_button:

    try:

        st.session_state.review_status = "PENDING"
        st.session_state.edit_mode = False

        with st.spinner(
            "Analyzing evidence and generating diagnosis..."
        ):

            result = diagnose(
                st.session_state.selected_case
            )

        st.session_state.diagnosis_result = result

        st.rerun()

    except Exception as error:

        st.error("Diagnosis generation failed.")
        st.exception(error)


# =========================================================
# CASE OVERVIEW
# =========================================================

result = st.session_state.diagnosis_result

if result:

    case = result.get("case", {})
    checker_result = result.get("checker_result", {})
    diagnosis = result.get("diagnosis", {})

else:

    case = {}
    checker_result = {}
    diagnosis = {}


with overview_col:

    st.markdown(
        '<div class="panel">',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="panel-title">'
        '▣ &nbsp; Case Overview'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="panel-line"></div>',
        unsafe_allow_html=True,
    )

    metric1, metric2 = st.columns(2)

    with metric1:

        st.markdown(
            '<div class="metric-label">CASE ID</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f'<div class="metric-value">'
            f'{case.get("case_id", selected_case)}'
            f'</div>',
            unsafe_allow_html=True,
        )

    with metric2:

        severity = str(
            case.get(
                "severity",
                "N/A"
            )
        )

        st.markdown(
            '<div class="metric-label">SEVERITY</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f'<div class="metric-value severity-high">'
            f'{severity}'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div style="margin-top:12px;"></div>',
        unsafe_allow_html=True,
    )

    metric3, metric4 = st.columns(2)

    with metric3:

        st.markdown(
            '<div class="metric-label">OSI LAYER</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f'<div class="metric-value">'
            f'{diagnosis.get("osi_layer", "N/A")}'
            f'</div>',
            unsafe_allow_html=True,
        )

    with metric4:

        confidence = float(
            diagnosis.get(
                "confidence",
                0
            ) or 0
        )

        st.markdown(
            '<div class="metric-label">AI CONFIDENCE</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f'<div class="metric-value confidence-good">'
            f'{confidence:.0%}'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '</div>',
        unsafe_allow_html=True,
    )


# =========================================================
# MAIN CONTENT
# =========================================================

if result:

    left_col, right_col = st.columns(
        [3.2, 1],
        gap="small",
    )

    # =====================================================
    # LEFT SIDE
    # =====================================================

    with left_col:

        # -------------------------------------------------
        # REPORTED SYMPTOM
        # -------------------------------------------------

        st.markdown(
            '<div class="panel">',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="panel-title">'
            '💬 &nbsp; Reported Symptom'
            '</div>',
            unsafe_allow_html=True,
        )

        symptom = case.get(
            "symptom",
            "No symptom information available."
        )

        st.markdown(
            f'<div class="symptom-box">'
            f'{symptom}'
            f'</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True,
        )


        # -------------------------------------------------
        # TOPOLOGY
        # -------------------------------------------------

        st.markdown(
            '<div class="panel">',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="panel-title">'
            '♧ &nbsp; Topology'
            '</div>',
            unsafe_allow_html=True,
        )

        topology = case.get(
            "topology_note",
            "Topology information not available."
        )

        st.markdown(
            f'<div class="topology-text">'
            f'{topology}'
            f'</div>',
            unsafe_allow_html=True,
        )

        with st.expander(
            "View Cisco Show Output"
        ):

            st.code(
                str(
                    case.get(
                        "show_outputs",
                        ""
                    )
                ),
                language="text",
            )

        st.markdown(
            '</div>',
            unsafe_allow_html=True,
        )


        # -------------------------------------------------
        # DETERMINISTIC CHECKER
        # -------------------------------------------------

        st.markdown(
            '<div class="panel">',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="panel-title">'
            '🛡 &nbsp; Deterministic Rule Checker'
            '</div>',
            unsafe_allow_html=True,
        )

        checker_status = checker_result.get(
            "status",
            "UNKNOWN"
        )

        if checker_status == "ERRORS_DETECTED":

            st.warning(
                "The deterministic checker detected "
                "one or more potential issues."
            )

        else:

            st.success(
                "Deterministic checker completed successfully."
            )

        with st.expander(
            "View Checker Results"
        ):

            st.json(
                checker_result
            )

        st.markdown(
            '</div>',
            unsafe_allow_html=True,
        )


        # -------------------------------------------------
        # AI DIAGNOSIS
        # -------------------------------------------------

        st.markdown(
            '<div class="panel">',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="panel-title">'
            '✦ &nbsp; AI Diagnosis'
            '</div>',
            unsafe_allow_html=True,
        )

        diagnosis_left, confidence_col, evidence_col = st.columns(
            [1.4, 0.9, 1]
        )

        with diagnosis_left:

            st.markdown(
                '<div class="root-cause">'
                '<div class="root-title">'
                '● &nbsp; Root Cause'
                '</div>'
                f'<div class="root-text">'
                f'{diagnosis.get("root_cause", "N/A")}'
                '</div>'
                '</div>',
                unsafe_allow_html=True,
            )

        with confidence_col:

            confidence = float(
                diagnosis.get(
                    "confidence",
                    0
                ) or 0
            )

            st.markdown(
                '<div class="panel-title" '
                'style="font-size:13px;">'
                '◉ &nbsp; Confidence'
                '</div>',
                unsafe_allow_html=True,
            )

            st.progress(
                confidence
            )

            st.markdown(
                f'<span style="color:#b9c4d4;'
                f'font-size:11px;">'
                f'AI confidence: {confidence:.0%}'
                f'</span>',
                unsafe_allow_html=True,
            )

        with evidence_col:

            st.markdown(
                '<div class="panel-title" '
                'style="font-size:13px;">'
                '▤ &nbsp; Evidence'
                '</div>',
                unsafe_allow_html=True,
            )

            evidence = diagnosis.get(
                "evidence",
                []
            )

            if evidence:

                for item in evidence[:4]:

                    st.markdown(
                        f'<div class="evidence-item">'
                        f'• {item}'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

            else:

                st.caption(
                    "No evidence available."
                )


        # -------------------------------------------------
        # NEXT COMMAND
        # -------------------------------------------------

        st.markdown(
            '<div style="margin-top:15px;"></div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="panel-title">'
            '▣ &nbsp; Recommended Next Command'
            '</div>',
            unsafe_allow_html=True,
        )

        st.code(
            diagnosis.get(
                "next_command",
                ""
            ),
            language="text",
        )


        # -------------------------------------------------
        # FIX STEPS
        # -------------------------------------------------

        st.markdown(
            '<div class="panel-title">'
            '⚒ &nbsp; Proposed Fix Steps'
            '</div>',
            unsafe_allow_html=True,
        )

        fix_steps = diagnosis.get(
            "fix_steps",
            []
        )

        if fix_steps:

            step_columns = st.columns(
                min(
                    len(fix_steps),
                    3
                )
            )

            for index, step in enumerate(
                fix_steps
            ):

                with step_columns[
                    index % len(step_columns)
                ]:

                    st.markdown(
                        f'<div class="fix-step">'
                        f'<span class="step-number">'
                        f'{index + 1}'
                        f'</span>'
                        f'{step}'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

        st.markdown(
            '</div>',
            unsafe_allow_html=True,
        )


    # =====================================================
    # RIGHT SIDE — HUMAN REVIEW
    # =====================================================

    with right_col:

        st.markdown(
            '<div class="panel">',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="panel-title">'
            '♙ &nbsp; Human Review'
            '</div>',
            unsafe_allow_html=True,
        )

        status = st.session_state.review_status

        if status == "PENDING":

            st.markdown(
                '<div class="pending-box">'
                '◉ &nbsp; Pending Human Review'
                '</div>',
                unsafe_allow_html=True,
            )

        elif status == "APPROVED":

            st.success(
                "✓ Diagnosis Approved"
            )

        elif status == "REJECTED":

            st.error(
                "✕ Diagnosis Rejected"
            )

        elif status == "EDITED":

            st.info(
                "✎ Diagnosis Edited"
            )


        st.markdown(
            '<div style="margin-top:16px;"></div>',
            unsafe_allow_html=True,
        )

        human_comment = st.text_area(
            "Review Comments",
            placeholder=(
                "Provide notes, approval, "
                "or corrections for the diagnosis."
            ),
            height=110,
        )


        approve_col, edit_col, reject_col = st.columns(
            3
        )


        # -------------------------------------------------
        # APPROVE
        # -------------------------------------------------

        with approve_col:

            if st.button(
                "✓ Approve",
                use_container_width=True,
            ):

                try:

                    save_audit_log(
                        case_id=case["case_id"],
                        diagnosis=diagnosis,
                        human_decision="APPROVED",
                        human_comment=human_comment,
                    )

                    st.session_state.review_status = (
                        "APPROVED"
                    )

                    st.success(
                        "Diagnosis approved and recorded."
                    )

                    st.rerun()

                except Exception as error:

                    st.error(
                        "Failed to record approval."
                    )

                    st.exception(error)


        # -------------------------------------------------
        # EDIT
        # -------------------------------------------------

        with edit_col:

            if st.button(
                "✎ Edit",
                use_container_width=True,
            ):

                st.session_state.edit_mode = True


        # -------------------------------------------------
        # REJECT
        # -------------------------------------------------

        with reject_col:

            if st.button(
                "✕ Reject",
                use_container_width=True,
            ):

                try:

                    save_audit_log(
                        case_id=case["case_id"],
                        diagnosis=diagnosis,
                        human_decision="REJECTED",
                        human_comment=human_comment,
                    )

                    st.session_state.review_status = (
                        "REJECTED"
                    )

                    st.error(
                        "Diagnosis rejected and recorded."
                    )

                    st.rerun()

                except Exception as error:

                    st.error(
                        "Failed to record rejection."
                    )

                    st.exception(error)


        # -------------------------------------------------
        # EDIT FORM
        # -------------------------------------------------

        if st.session_state.edit_mode:

            st.divider()

            st.markdown(
                "**Edit Diagnosis**"
            )

            edited_root = st.text_area(
                "Root Cause",
                value=diagnosis.get(
                    "root_cause",
                    ""
                ),
            )

            edited_layer = st.text_input(
                "OSI Layer",
                value=diagnosis.get(
                    "osi_layer",
                    ""
                ),
            )

            edited_confidence = st.number_input(
                "Confidence",
                min_value=0.0,
                max_value=1.0,
                value=float(
                    diagnosis.get(
                        "confidence",
                        0
                    )
                ),
                step=0.01,
            )

            edited_command = st.text_input(
                "Next Command",
                value=diagnosis.get(
                    "next_command",
                    ""
                ),
            )

            edited_evidence = st.text_area(
                "Evidence",
                value="\n".join(
                    diagnosis.get(
                        "evidence",
                        []
                    )
                ),
            )

            edited_steps = st.text_area(
                "Fix Steps",
                value="\n".join(
                    diagnosis.get(
                        "fix_steps",
                        []
                    )
                ),
            )

            if st.button(
                "Save Edited Diagnosis",
                type="primary",
                use_container_width=True,
            ):

                edited_diagnosis = {
                    "root_cause": edited_root,
                    "osi_layer": edited_layer,
                    "confidence": edited_confidence,
                    "evidence": [
                        x.strip()
                        for x in edited_evidence.splitlines()
                        if x.strip()
                    ],
                    "next_command": edited_command,
                    "fix_steps": [
                        x.strip()
                        for x in edited_steps.splitlines()
                        if x.strip()
                    ],
                }

                try:

                    save_audit_log(
                        case_id=case["case_id"],
                        diagnosis=edited_diagnosis,
                        human_decision="EDITED",
                        human_comment=human_comment,
                    )

                    st.session_state.diagnosis_result[
                        "diagnosis"
                    ] = edited_diagnosis

                    st.session_state.review_status = (
                        "EDITED"
                    )

                    st.session_state.edit_mode = False

                    st.success(
                        "Edited diagnosis saved."
                    )

                    st.rerun()

                except Exception as error:

                    st.error(
                        "Failed to save edited diagnosis."
                    )

                    st.exception(error)

        st.markdown(
            '</div>',
            unsafe_allow_html=True,
        )


else:

    st.info(
        "Select a case and click "
        "'Run Diagnosis' to begin."
    )