import io
from datetime import datetime

import pandas as pd
import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="OMD Operations Portal",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# AUTO REFRESH
# ============================================================

try:
    from streamlit_autorefresh import st_autorefresh

    st_autorefresh(
        interval=30000,
        key="omd_refresh"
    )

except ImportError:
    pass


# ============================================================
# EXPECTED COLUMNS
# ============================================================

EXPECTED_COLUMNS = [
    "Cluster",
    "Ticket No.",
    "Status",
    "Assigned To",
    "Country",
    "Request Type",
    "Upload Date",
    "Due Date",
    "Due In",
    "Team"
]


# ============================================================
# SESSION STATE
# ============================================================

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=EXPECTED_COLUMNS)

if "uploaded" not in st.session_state:
    st.session_state.uploaded = False

if "current_page" not in st.session_state:
    st.session_state.current_page = 1

if "selected_transfer" not in st.session_state:
    st.session_state.selected_transfer = "Select action"

if "message" not in st.session_state:
    st.session_state.message = ""


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>

:root {
    --bosch-blue: #00679d;
    --bosch-blue-dark: #004f79;
    --bosch-red: #e20015;
    --bosch-green: #00a982;
    --bosch-purple: #7054c7;
    --bosch-yellow: #f7d900;

    --background: #f3f6f8;
    --white: #ffffff;

    --text: #26364d;
    --muted: #778493;

    --border: #dce4ea;
    --light-blue: #eef7fb;
}


/* ============================================================
   REMOVE STREAMLIT DEFAULT UI
   ============================================================ */

#MainMenu,
header,
footer,
[data-testid="stToolbar"],
[data-testid="stDecoration"] {
    display: none !important;
}


[data-testid="stAppViewContainer"] {
    background: var(--background);
}


.block-container {
    max-width: 100% !important;
    padding: 0 0 40px 0 !important;
}


* {
    box-sizing: border-box;
    font-family: Arial, "Segoe UI", sans-serif;
}


/* ============================================================
   TOP BOSCH MULTI-COLOR STRIP
   ============================================================ */

.bosch-strip {
    height: 13px;

    background:
        linear-gradient(
            90deg,
            #a71930 0%,
            #a71930 24%,

            #7054c7 24%,
            #7054c7 35%,

            #244987 35%,
            #244987 52%,

            #18a2c7 52%,
            #18a2c7 71%,

            #00a982 71%,
            #00a982 88%,

            #79b940 88%,
            #79b940 100%
        );
}


/* ============================================================
   HEADER
   ============================================================ */

.top-header {
    height: 112px;

    background: white;

    display: flex;
    align-items: center;

    padding: 0 30px;

    border-bottom: 1px solid #e4e8ec;

    box-shadow:
        0 2px 10px rgba(0, 0, 0, 0.05);
}


/* ============================================================
   OMD LOGO
   ============================================================ */

.omd-brand {
    display: flex;
    align-items: center;
    gap: 14px;

    min-width: 255px;
}


.omd-logo {
    width: 62px;
    height: 62px;

    border-radius: 50%;

    background: #eef8fc;

    border: 3px solid var(--bosch-blue);

    display: flex;
    align-items: center;
    justify-content: center;

    color: var(--bosch-blue);

    font-size: 30px;
}


.omd-title {
    color: #26364d;
    font-size: 23px;
    font-weight: 700;
}


.omd-subtitle {
    color: #7d8791;
    font-size: 13px;
    margin-top: 5px;
}


/* ============================================================
   NAVIGATION
   ============================================================ */

.navigation {
    display: flex;
    align-items: center;

    gap: 42px;

    flex: 1;

    height: 100%;
}


.navigation-item {
    height: 100%;

    display: flex;
    align-items: center;

    position: relative;

    color: #29374b;

    font-size: 18px;
    font-weight: 700;

    white-space: nowrap;
}


.navigation-item.active {
    color: var(--bosch-blue);
}


.navigation-item.active::after {
    content: "";

    position: absolute;

    left: 0;
    right: 0;

    bottom: 20px;

    height: 4px;

    border-radius: 4px;

    background: var(--bosch-blue);
}


/* ============================================================
   HEADER ICONS
   ============================================================ */

.header-icons {
    display: flex;

    align-items: center;

    gap: 18px;

    color: #687792;

    font-size: 21px;

    margin-right: 20px;
}


.header-divider {
    width: 1px;

    height: 55px;

    background: #e0e4e8;

    margin-right: 22px;
}


/* ============================================================
   BOSCH BRAND
   ============================================================ */

.bosch-logo {
    min-width: 150px;

    text-align: right;
}


.bosch-logo b {
    display: block;

    color: var(--bosch-red);

    font-size: 31px;

    letter-spacing: -1px;
}


.bosch-logo small {
    display: block;

    color: #333;

    font-size: 13px;

    margin-top: 5px;
}


/* ============================================================
   MAIN LAYOUT
   ============================================================ */

.main-layout {
    display: grid;

    grid-template-columns: 190px 1fr;

    min-height: calc(100vh - 125px);
}


/* ============================================================
   CUSTOM LEFT SIDEBAR
   ============================================================ */

.custom-sidebar {
    background: white;

    border-right: 1px solid #e0e6eb;

    padding-top: 15px;
}


.sidebar-heading {
    padding: 12px 20px 15px;

    color: #89939e;

    font-size: 11px;

    font-weight: 700;

    text-transform: uppercase;

    letter-spacing: 0.7px;
}


.sidebar-item {
    height: 55px;

    display: flex;

    align-items: center;

    gap: 12px;

    padding: 0 18px;

    color: #354458;

    font-size: 14px;

    font-weight: 600;

    border-left: 4px solid transparent;

    transition: 0.2s;
}


.sidebar-item:hover {
    background: #f1f8fb;
}


.sidebar-item.active {
    background: var(--bosch-blue);

    color: white;

    border-left-color: var(--bosch-blue-dark);
}


.sidebar-icon {
    width: 25px;

    text-align: center;

    font-size: 18px;
}


.sidebar-count {
    margin-left: auto;

    font-size: 12px;

    opacity: 0.85;
}


/* ============================================================
   MAIN CONTENT
   ============================================================ */

.main-content {
    padding: 25px 28px 40px;
}


/* ============================================================
   INFORMATION BAR
   ============================================================ */

.info-bar {
    min-height: 52px;

    background: #fffde1;

    border: 1px solid #efe18a;

    border-left: 5px solid #d6bd00;

    border-radius: 6px;

    display: flex;

    align-items: center;

    gap: 13px;

    padding: 0 18px;

    color: #625b00;

    font-size: 14px;

    margin-bottom: 22px;
}


.info-icon {
    width: 28px;
    height: 28px;

    border: 2px solid #625b00;

    border-radius: 50%;

    display: flex;
    align-items: center;
    justify-content: center;

    font-weight: 700;
}


/* ============================================================
   ACTION BOX
   ============================================================ */

.action-card {
    background: white;

    border: 1px solid var(--border);

    border-radius: 8px;

    box-shadow:
        0 4px 18px rgba(35, 67, 95, 0.07);

    margin-bottom: 26px;

    overflow: visible;
}


/* COLOR LINE ON TOP OF ACTION BOX */

.action-color-line {
    height: 5px;

    border-radius: 8px 8px 0 0;

    background:
        linear-gradient(
            90deg,
            #087bb0 0%,
            #087bb0 22%,

            #7054c7 22%,
            #7054c7 42%,

            #e1a11e 42%,
            #e1a11e 61%,

            #00a58a 61%,
            #00a58a 82%,

            #79b940 82%,
            #79b940 100%
        );
}


/* ============================================================
   ACTION CONTENT
   ============================================================ */

.action-content {
    padding: 17px 20px 19px;
}


.action-label {
    color: #7a8591;

    font-size: 11px;

    font-weight: 700;

    margin-bottom: 7px;

    white-space: nowrap;
}


/* ============================================================
   STREAMLIT WIDGET STYLING
   ============================================================ */

div[data-testid="stButton"] > button {
    height: 43px !important;

    border-radius: 6px !important;

    border: 1px solid #a5cddd !important;

    background: #f4f9fc !important;

    color: #0871a2 !important;

    font-weight: 700 !important;

    font-size: 13px !important;

    transition: 0.2s !important;
}


div[data-testid="stButton"] > button:hover {
    background: #e6f4fa !important;

    border-color: #087bb0 !important;

    color: #005a82 !important;
}


/* Assign */

.assign-button-container div[data-testid="stButton"] > button {
    background: #087bb0 !important;

    border-color: #087bb0 !important;

    color: white !important;
}


.assign-button-container div[data-testid="stButton"] > button:hover {
    background: #005f88 !important;

    color: white !important;
}


/* ============================================================
   SELECTBOX
   ============================================================ */

div[data-testid="stSelectbox"] {
    margin-top: 0 !important;
}


div[data-testid="stSelectbox"] > div > div {
    min-height: 43px !important;

    border-radius: 0 6px 6px 0 !important;

    border-color: #087bb0 !important;
}


/* ============================================================
   TEXT INPUT
   ============================================================ */

div[data-testid="stTextInput"] input {
    height: 43px !important;

    border-radius: 5px !important;

    border: none !important;

    border-bottom: 1px solid #aeb7c1 !important;

    background: white !important;

    color: #354458 !important;

    font-size: 13px !important;
}


div[data-testid="stTextInput"] input:focus {
    border-bottom: 2px solid var(--bosch-blue) !important;

    box-shadow: none !important;
}


/* ============================================================
   FILE UPLOAD
   ============================================================ */

.upload-section {
    background: white;

    border: 1px solid var(--border);

    border-radius: 8px;

    padding: 17px 20px;

    margin-bottom: 24px;

    box-shadow:
        0 3px 13px rgba(35, 67, 95, 0.05);
}


.upload-title {
    font-size: 15px;

    font-weight: 700;

    color: #263b58;

    margin-bottom: 5px;
}


.upload-subtitle {
    color: #7c8793;

    font-size: 12px;

    margin-bottom: 12px;
}


/* ============================================================
   REQUEST HEADER
   ============================================================ */

.request-header {
    display: flex;

    justify-content: space-between;

    align-items: center;

    margin-bottom: 11px;

    padding: 0 2px;
}


.request-title {
    color: #263b58;

    font-size: 19px;

    font-weight: 700;
}


.updated-time {
    color: #788493;

    font-size: 12px;
}


/* ============================================================
   TABLE
   ============================================================ */

.table-card {
    background: white;

    border: 1px solid #dce4eb;

    border-radius: 7px;

    overflow-x: auto;

    box-shadow:
        0 3px 13px rgba(30, 65, 100, 0.05);
}


.omd-table {
    width: 100%;

    border-collapse: collapse;

    min-width: 1100px;

    font-size: 13px;
}


.omd-table th {
    padding: 13px 10px;

    background: #f5f8fa;

    color: #354458;

    border-bottom: 1px solid #dce4eb;

    font-size: 12px;

    font-weight: 800;

    text-align: left;

    white-space: nowrap;
}


.omd-table td {
    padding: 12px 10px;

    color: #4a5869;

    border-bottom: 1px solid #edf0f3;

    white-space: nowrap;
}


.omd-table tr:hover td {
    background: #f5fbfd;
}


/* ============================================================
   CLUSTER BADGE
   ============================================================ */

.cluster-badge {
    display: inline-flex;

    align-items: center;

    justify-content: center;

    min-width: 48px;

    padding: 6px 11px;

    border-radius: 18px;

    background: #009bd0;

    color: white;

    font-weight: 700;

    font-size: 11px;
}


/* ============================================================
   STATUS
   ============================================================ */

.status-open {
    color: #0871a2;

    font-weight: 700;
}


.status-new {
    color: #008c72;

    font-weight: 700;
}


.status-hold {
    color: #a56c00;

    font-weight: 700;
}


.status-clarification {
    color: #7054c7;

    font-weight: 700;
}


/* ============================================================
   NO DATA
   ============================================================ */

.no-data {
    height: 180px;

    display: flex;

    flex-direction: column;

    align-items: center;

    justify-content: center;

    gap: 9px;

    color: #8a97a5;
}


.no-data-icon {
    font-size: 34px;

    opacity: 0.55;
}


.no-data-title {
    font-size: 14px;

    font-weight: 700;
}


.no-data-text {
    font-size: 12px;
}


/* ============================================================
   PAGINATION
   ============================================================ */

.pagination-info {
    text-align: center;

    color: #7c8792;

    font-size: 12px;

    margin-top: 12px;
}


/* ============================================================
   SUCCESS MESSAGE
   ============================================================ */

.action-message {
    background: #eef9f5;

    border: 1px solid #a8ddce;

    border-left: 4px solid #00a982;

    color: #176b5a;

    padding: 10px 14px;

    border-radius: 5px;

    margin-bottom: 18px;

    font-size: 13px;
}


/* ============================================================
   RESPONSIVE
   ============================================================ */

@media(max-width: 1250px) {

    .navigation {
        gap: 20px;
    }

    .navigation-item {
        font-size: 15px;
    }

    .omd-brand {
        min-width: 210px;
    }

    .action-content {
        padding: 15px;
    }
}


@media(max-width: 950px) {

    .main-layout {
        grid-template-columns: 1fr;
    }

    .custom-sidebar {
        display: none;
    }

    .navigation-item:nth-child(3) {
        display: none;
    }

    .bosch-logo {
        min-width: 100px;
    }

    .bosch-logo b {
        font-size: 23px;
    }

    .main-content {
        padding: 18px;
    }
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
<div class="bosch-strip"></div>

<div class="top-header">

    <div class="omd-brand">

        <div class="omd-logo">
            ⚙
        </div>

        <div>
            <div class="omd-title">
                OMD Hub
            </div>

            <div class="omd-subtitle">
                Smart Operations
            </div>
        </div>

    </div>


    <div class="navigation">

        <div class="navigation-item active">
            Home
        </div>

        <div class="navigation-item">
            GVMD Allocation
        </div>

        <div class="navigation-item">
            Delivery Track Portal
        </div>

        <div class="navigation-item">
            Reports
        </div>

    </div>


    <div class="header-icons">
        <span>▣</span>
        <span>◇</span>
        <span>●</span>
    </div>


    <div class="header-divider"></div>


    <div class="bosch-logo">

        <b>BOSCH</b>

        <small>
            Invented for life
        </small>

    </div>

</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# DATA UPLOAD
# ============================================================

uploaded_file = None


# ============================================================
# MAIN LAYOUT
# ============================================================

st.markdown(
    '<div class="main-layout">',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR DATA COUNTS
# ============================================================

df = st.session_state.df.copy()

all_count = len(df)

open_count = int(
    (df["Status"].astype(str).str.lower() == "open").sum()
)

new_count = int(
    (df["Status"].astype(str).str.lower() == "new").sum()
)

hold_count = int(
    (df["Status"].astype(str).str.lower() == "hold").sum()
)

clarification_count = int(
    (
        df["Status"]
        .astype(str)
        .str.lower()
        .eq("in clarification")
    ).sum()
)

in_progress_count = int(
    (
        df["Status"]
        .astype(str)
        .str.lower()
        .eq("in progress")
    ).sum()
)

esm_count = int(
    (
        df["Cluster"]
        .astype(str)
        .str.upper()
        .eq("ESM")
    ).sum()
)


# ============================================================
# SIDEBAR
# ============================================================

sidebar_html = f"""
<div class="custom-sidebar">

    <div class="sidebar-heading">
        OMD Requests
    </div>

    <div class="sidebar-item active">
        <span class="sidebar-icon">⚙</span>
        <span>All</span>
        <span class="sidebar-count">{all_count}</span>
    </div>

    <div class="sidebar-item">
        <span class="sidebar-icon">□</span>
        <span>Open</span>
        <span class="sidebar-count">{open_count}</span>
    </div>

    <div class="sidebar-item">
        <span class="sidebar-icon">＋</span>
        <span>New</span>
        <span class="sidebar-count">{new_count}</span>
    </div>

    <div class="sidebar-item">
        <span class="sidebar-icon">✓</span>
        <span>Hold</span>
        <span class="sidebar-count">{hold_count}</span>
    </div>

    <div class="sidebar-item">
        <span class="sidebar-icon">?</span>
        <span>In Clarification</span>
        <span class="sidebar-count">{clarification_count}</span>
    </div>

    <div class="sidebar-item">
        <span class="sidebar-icon">↻</span>
        <span>In Progress</span>
        <span class="sidebar-count">{in_progress_count}</span>
    </div>

    <div class="sidebar-item">
        <span class="sidebar-icon">▤</span>
        <span>ESM</span>
        <span class="sidebar-count">{esm_count}</span>
    </div>

</div>
"""


st.markdown(
    sidebar_html,
    unsafe_allow_html=True
)


# ============================================================
# CONTENT
# ============================================================

st.markdown(
    '<main class="main-content">',
    unsafe_allow_html=True
)


# ============================================================
# INFORMATION BAR
# ============================================================

st.markdown(
    """
<div class="info-bar">

    <div class="info-icon">
        !
    </div>

    <div>
        <b>Information:</b>
        Welcome to the OMD Allocation Portal.
        Upload the latest GVMD files and review allocations before export.
    </div>

</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# ACTION CARD
# ============================================================

st.markdown(
    """
<div class="action-card">

    <div class="action-color-line"></div>

    <div class="action-content">

        <div style="
            color:#263b58;
            font-size:15px;
            font-weight:700;
            margin-bottom:14px;
        ">
            Ticket Actions
        </div>

    </div>

</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# ACTION CONTROLS
# ============================================================

action_cols = st.columns(
    [1.45, 1.75, 1.05, 1.9, 1.35, 1.25, 1.45],
    gap="small"
)


# ------------------------------------------------------------
# TRANSFER + DROPDOWN
# ------------------------------------------------------------

with action_cols[0]:

    st.markdown(
        '<div class="action-label">Transfer</div>',
        unsafe_allow_html=True
    )

    transfer_cols = st.columns([2.4, 0.85], gap="small")

    with transfer_cols[0]:

        transfer_clicked = st.button(
            "⇄ Transfer",
            key="transfer_button",
            use_container_width=True
        )

    with transfer_cols[1]:

        transfer_option = st.selectbox(
            "Transfer",
            [
                "Select",
                "Ntid",
                "ESM",
                "PISA",
                "PM7"
            ],
            key="transfer_dropdown",
            label_visibility="collapsed"
        )


# ------------------------------------------------------------
# ASSIGN
# ------------------------------------------------------------

with action_cols[1]:

    st.markdown(
        '<div class="action-label">Assign</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="assign-button-container">',
        unsafe_allow_html=True
    )

    assign_clicked = st.button(
        "♙  Assign",
        key="assign_button",
        use_container_width=True
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ------------------------------------------------------------
# USER INPUT
# ------------------------------------------------------------

with action_cols[2]:

    st.markdown(
        '<div class="action-label">User</div>',
        unsafe_allow_html=True
    )

    assigned_user = st.text_input(
        "User",
        placeholder="Name / Email",
        key="assigned_user",
        label_visibility="collapsed"
    )


# ------------------------------------------------------------
# SELF ASSIGN
# ------------------------------------------------------------

with action_cols[3]:

    st.markdown(
        '<div class="action-label">Self Assign</div>',
        unsafe_allow_html=True
    )

    self_assign_clicked = st.button(
        "♙  Self Assign",
        key="self_assign_button",
        use_container_width=True
    )


# ------------------------------------------------------------
# SEARCH
# ------------------------------------------------------------

with action_cols[4]:

    st.markdown(
        '<div class="action-label">Search</div>',
        unsafe_allow_html=True
    )

    search_text = st.text_input(
        "Search",
        placeholder="⌕  Search tickets...",
        key="search_box",
        label_visibility="collapsed"
    )


# ------------------------------------------------------------
# UPLOAD
# ------------------------------------------------------------

with action_cols[5]:

    st.markdown(
        '<div class="action-label">GVMD File</div>',
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "GVMD File",
        type=["xlsx", "xls", "csv"],
        key="gvmd_upload",
        label_visibility="collapsed"
    )


# ------------------------------------------------------------
# EXCEL DOWNLOAD
# ------------------------------------------------------------

with action_cols[6]:

    st.markdown(
        '<div class="action-label">Export</div>',
        unsafe_allow_html=True
    )

    if not df.empty:

        excel_output = io.BytesIO()

        with pd.ExcelWriter(
            excel_output,
            engine="openpyxl"
        ) as writer:

            df.to_excel(
                writer,
                index=False,
                sheet_name="OMD Tickets"
            )

            worksheet = writer["OMD Tickets"]

            for column_cells in worksheet.columns:

                max_length = 0

                column_letter = (
                    column_cells[0].column_letter
                )

                for cell in column_cells:

                    if cell.value is not None:

                        max_length = max(
                            max_length,
                            len(str(cell.value))
                        )

                worksheet.column_dimensions[
                    column_letter
                ].width = min(
                    max_length + 3,
                    35
                )

        excel_output.seek(0)

        st.download_button(
            label="📊 Excel",
            data=excel_output.getvalue(),
            file_name="OMD_Ticket_Allocation.xlsx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            ),
            use_container_width=True,
            key="excel_download"
        )

    else:

        st.download_button(
            label="📊 Excel",
            data=b"",
            file_name="OMD_Ticket_Allocation.xlsx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            ),
            disabled=True,
            use_container_width=True,
            key="excel_download_empty"
        )


# ============================================================
# HANDLE EXCEL UPLOAD
# ============================================================

if uploaded_file is not None:

    try:

        file_name = uploaded_file.name.lower()

        if file_name.endswith(".csv"):

            uploaded_df = pd.read_csv(
                uploaded_file
            )

        else:

            uploaded_df = pd.read_excel(
                uploaded_file
            )


        # ----------------------------------------------------
        # CLEAN COLUMN NAMES
        # ----------------------------------------------------

        uploaded_df.columns = [
            str(column).strip()
            for column in uploaded_df.columns
        ]


        # ----------------------------------------------------
        # MAP COMMON COLUMN NAMES
        # ----------------------------------------------------

        column_mapping = {}

        for column in uploaded_df.columns:

            clean_column = (
                str(column)
                .strip()
                .lower()
                .replace("_", " ")
            )

            if clean_column in [
                "cluster",
                "cluster type"
            ]:

                column_mapping[column] = "Cluster"

            elif clean_column in [
                "ticket no",
                "ticket no.",
                "ticket number",
                "ticket"
            ]:

                column_mapping[column] = "Ticket No."

            elif clean_column == "status":

                column_mapping[column] = "Status"

            elif clean_column in [
                "assigned to",
                "assigned"
            ]:

                column_mapping[column] = "Assigned To"

            elif clean_column == "country":

                column_mapping[column] = "Country"

            elif clean_column in [
                "request type",
                "request"
            ]:

                column_mapping[column] = "Request Type"

            elif clean_column in [
                "upload date",
                "uploaded date"
            ]:

                column_mapping[column] = "Upload Date"

            elif clean_column in [
                "due date"
            ]:

                column_mapping[column] = "Due Date"

            elif clean_column in [
                "due in"
            ]:

                column_mapping[column] = "Due In"

            elif clean_column == "team":

                column_mapping[column] = "Team"


        uploaded_df = uploaded_df.rename(
            columns=column_mapping
        )


        # ----------------------------------------------------
        # ADD MISSING COLUMNS
        # ----------------------------------------------------

        for column in EXPECTED_COLUMNS:

            if column not in uploaded_df.columns:

                uploaded_df[column] = ""


        # ----------------------------------------------------
        # KEEP EXPECTED COLUMNS
        # ----------------------------------------------------

        uploaded_df = uploaded_df[
            EXPECTED_COLUMNS
        ]


        st.session_state.df = uploaded_df

        st.session_state.uploaded = True

        df = uploaded_df.copy()


        st.session_state.message = (
            f"Successfully loaded {len(df)} ticket(s) "
            f"from {uploaded_file.name}."
        )


    except Exception as error:

        st.error(
            f"Unable to read the uploaded file: {error}"
        )


# ============================================================
# ACTION RESPONSES
# ============================================================

if transfer_clicked:

    if transfer_option == "Select":

        st.warning(
            "Please select a transfer destination."
        )

    elif df.empty:

        st.warning(
            "Please upload a GVMD/OMD Excel file first."
        )

    else:

        st.session_state.message = (
            f"Transfer selected → {transfer_option}"
        )


if assign_clicked:

    if df.empty:

        st.warning(
            "Please upload a file before assigning tickets."
        )

    elif not assigned_user.strip():

        st.warning(
            "Please enter a name or email address."
        )

    else:

        st.session_state.message = (
            f"Assignment selected for {assigned_user}."
        )


if self_assign_clicked:

    if df.empty:

        st.warning(
            "Please upload a file before self assignment."
        )

    else:

        st.session_state.message = (
            "Self Assign selected."
        )


# ============================================================
# SHOW ACTION MESSAGE
# ============================================================

if st.session_state.message:

    st.markdown(
        f"""
        <div class="action-message">
            ✓ {st.session_state.message}
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# UPLOAD AREA
# ============================================================

st.markdown(
    """
<div class="upload-section">

    <div class="upload-title">
        GVMD / OMD Excel Upload
    </div>

    <div class="upload-subtitle">
        Upload the latest Excel or CSV file to populate the ticket table.
    </div>

</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# SEARCH FILTER
# ============================================================

display_df = df.copy()


if search_text.strip():

    search_value = search_text.strip().lower()

    mask = display_df.astype(str).apply(
        lambda column:
        column.str.lower().str.contains(
            search_value,
            na=False
        )
    ).any(axis=1)

    display_df = display_df[mask]


# ============================================================
# REQUEST HEADER
# ============================================================

st.markdown(
    f"""
    <div class="request-header">

        <div class="request-title">
            All OMD Requests
        </div>

        <div class="updated-time">
            Updated {
                datetime.now().strftime(
                    "%d/%m/%Y %I:%M %p"
                )
            }
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TABLE
# ============================================================

if display_df.empty:

    st.markdown(
        """
        <div class="table-card">

            <table class="omd-table">

                <thead>

                    <tr>

                        <th>○</th>
                        <th>Cluster Type</th>
                        <th>Ticket No.</th>
                        <th>Status</th>
                        <th>Assigned To</th>
                        <th>Country</th>
                        <th>Request Type</th>
                        <th>Upload Date</th>
                        <th>Due Date</th>
                        <th>Due In</th>
                        <th>Team ＋ ▼</th>

                    </tr>

                </thead>

            </table>

            <div class="no-data">

                <div class="no-data-icon">
                    ▤
                </div>

                <div class="no-data-title">
                    No data available
                </div>

                <div class="no-data-text">
                    Upload the latest GVMD Excel file to view OMD requests.
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


else:

    # --------------------------------------------------------
    # PAGINATION
    # --------------------------------------------------------

    rows_per_page = 10

    total_rows = len(display_df)

    total_pages = max(
        1,
        (total_rows + rows_per_page - 1)
        // rows_per_page
    )


    if st.session_state.current_page > total_pages:

        st.session_state.current_page = 1


    start_index = (
        st.session_state.current_page - 1
    ) * rows_per_page

    end_index = start_index + rows_per_page

    page_df = display_df.iloc[
        start_index:end_index
    ]


    # --------------------------------------------------------
    # TABLE HTML
    # --------------------------------------------------------

    rows_html = ""


    for _, row in page_df.iterrows():

        status = str(
            row["Status"]
        ).strip()


        status_lower = status.lower()


        status_class = ""


        if status_lower == "open":

            status_class = "status-open"


        elif status_lower == "new":

            status_class = "status-new"


        elif status_lower == "hold":

            status_class = "status-hold"


        elif status_lower == "in clarification":

            status_class = "status-clarification"


        rows_html += f"""
        <tr>

            <td>
                □
            </td>

            <td>
                <span class="cluster-badge">
                    {row["Cluster"]}
                </span>
            </td>

            <td>
                ★ {row["Ticket No."]}
            </td>

            <td class="{status_class}">
                {status}
            </td>

            <td>
                {row["Assigned To"]}
            </td>

            <td>
                {row["Country"]}
            </td>

            <td>
                {row["Request Type"]}
            </td>

            <td>
                {row["Upload Date"]}
            </td>

            <td>
                {row["Due Date"]}
            </td>

            <td>
                {row["Due In"]}
            </td>

            <td>
                {row["Team"]}
            </td>

        </tr>
        """


    st.markdown(
        f"""
        <div class="table-card">

            <table class="omd-table">

                <thead>

                    <tr>

                        <th>○</th>
                        <th>Cluster Type</th>
                        <th>Ticket No.</th>
                        <th>Status</th>
                        <th>Assigned To</th>
                        <th>Country</th>
                        <th>Request Type</th>
                        <th>Upload Date</th>
                        <th>Due Date</th>
                        <th>Due In</th>
                        <th>Team ＋ ▼</th>

                    </tr>

                </thead>

                <tbody>

                    {rows_html}

                </tbody>

            </table>

        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # PAGINATION CONTROLS
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="pagination-info">

            Showing
            {start_index + 1}
            -
            {min(end_index, total_rows)}
            of
            {total_rows}
            tickets

        </div>
        """,
        unsafe_allow_html=True
    )


    pagination_cols = st.columns(
        [1, 1, 1, 1, 1, 1, 1]
    )


    with pagination_cols[1]:

        if st.button(
            "«",
            key="first_page",
            use_container_width=True
        ):

            st.session_state.current_page = 1

            st.rerun()


    with pagination_cols[2]:

        if st.button(
            "‹",
            key="previous_page",
            use_container_width=True
        ):

            if st.session_state.current_page > 1:

                st.session_state.current_page -= 1

                st.rerun()


    with pagination_cols[3]:

        st.button(
            str(st.session_state.current_page),
            key="current_page_display",
            disabled=True,
            use_container_width=True
        )


    with pagination_cols[4]:

        if st.button(
            "›",
            key="next_page",
            use_container_width=True
        ):

            if (
                st.session_state.current_page
                < total_pages
            ):

                st.session_state.current_page += 1

                st.rerun()


    with pagination_cols[5]:

        if st.button(
            "»",
            key="last_page",
            use_container_width=True
        ):

            st.session_state.current_page = total_pages

            st.rerun()


# ============================================================
# CLOSE MAIN CONTENT
# ============================================================

st.markdown(
    """
    </main>
    </div>
    """,
    unsafe_allow_html=True
)
