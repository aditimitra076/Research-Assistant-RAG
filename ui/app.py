import sys
import os
from uuid import uuid4


ui_path = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(ui_path)

for import_path in (ui_path, project_root):
    if import_path not in sys.path:
        sys.path.insert(0, import_path)

import streamlit as st

from pages.projects import(
    show_projects
)

from pages.workspace import(
    show_workspace
)

from ui.components.icons import icon_svg
from modules.generator import is_hf_token_configured


st.set_page_config(
    page_title="Research Assistant",
    layout="wide"
)

st.markdown(
    """
    <style>
    :root {
        color-scheme: dark;
        --page: #111719;
        --surface: #192124;
        --surface-raised: #202a2e;
        --surface-strong: #263236;
        --border: #354448;
        --text: #edf3f1;
        --muted: #aab8b5;
        --accent: #78d6bd;
        --accent-strong: #9be5d1;
    }
    [data-testid="stAppViewContainer"] {
        background: var(--page);
        color: var(--text);
    }

    [data-testid="stHeader"] {
        background: var(--page);
    }

    .block-container {
        max-width: 1120px;
        padding: 2.25rem 2.5rem 5rem;
    }

    [data-testid="stSidebar"] {
        background: #151d20;
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 1rem;
    }

    .brand-lockup {
        display: flex;
        align-items: center;
        gap: 0.7rem;
        color: var(--text);
        font-size: 1.15rem;
        font-weight: 700;
    }

    .brand-lockup .ui-icon {
        width: 1.5rem;
        height: 1.5rem;
        color: var(--accent);
    }

    .ui-icon {
        display: inline-block;
        width: 1.2rem;
        height: 1.2rem;
        flex: 0 0 auto;
        vertical-align: middle;
    }

    .page-hero {
        display: flex;
        align-items: flex-start;
        gap: 1.1rem;
        margin: 0 0 2rem;
        padding: 1.6rem 1.75rem;
        background: linear-gradient(110deg, #1b272a 0%, #182124 72%);
        border: 1px solid var(--border);
        border-left: 4px solid var(--accent);
        border-radius: 12px;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.16);
    }

    .page-hero .hero-icon {
        display: grid;
        width: 3rem;
        height: 3rem;
        flex: 0 0 3rem;
        place-items: center;
        color: var(--accent);
        background: #263633;
        border: 1px solid #3b5d54;
        border-radius: 9px;
    }

    .page-hero .hero-icon .ui-icon {
        width: 1.55rem;
        height: 1.55rem;
    }

    .page-hero .eyebrow {
        margin: 0 0 0.35rem;
        color: var(--accent);
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
    }

    .page-hero h1 {
        margin: 0;
        color: var(--text);
        font-size: 2.2rem;
        line-height: 1.2;
    }

    .page-hero p {
        margin: 0.55rem 0 0;
        color: var(--muted);
        font-size: 1.05rem;
        line-height: 1.6;
    }

    .section-heading {
        display: flex;
        align-items: center;
        gap: 0.65rem;
        margin: 0 0 0.9rem;
        color: var(--text);
        font-size: 1.2rem;
        font-weight: 650;
    }

    .section-heading .ui-icon {
        color: var(--accent);
    }

    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3 {
        color: var(--text);
        font-weight: 650;
        letter-spacing: 0;
    }

    [data-testid="stMarkdownContainer"] h1 {
        font-size: 2rem;
        line-height: 1.2;
    }

    [data-testid="stMarkdownContainer"] h2 {
        font-size: 1.55rem;
    }

    [data-testid="stHeadingWithActionElements"] h2 {
        font-size: 1.65rem;
    }

    [data-testid="stMarkdownContainer"] p,
    [data-testid="stCaptionContainer"] {
        color: var(--muted);
        font-size: 0.98rem;
        line-height: 1.65;
    }

    [data-testid="stMetric"] {
        min-height: 6rem;
        padding: 1.1rem 1.2rem;
        background: var(--surface-raised);
        border: 1px solid var(--border);
        border-radius: 10px;
    }

    [data-testid="stMetricLabel"] {
        color: var(--muted);
    }

    [data-testid="stMetricValue"] {
        color: var(--text);
        font-size: 1.65rem;
        font-weight: 700;
    }

    .stTextInput input,
    [data-testid="stChatInput"] textarea {
        color: var(--text);
        background: #101719;
        border-color: var(--border);
        border-radius: 9px;
        font-size: 1rem;
    }

    .stTextInput input:focus,
    [data-testid="stChatInput"] textarea:focus {
        border-color: var(--accent);
        box-shadow: 0 0 0 2px rgba(120, 214, 189, 0.22);
    }

    .stButton > button {
        min-height: 2.85rem;
        padding: 0.55rem 1rem;
        color: var(--text);
        background: var(--surface-raised);
        border: 1px solid var(--border);
        border-radius: 9px;
        font-weight: 600;
        transition: border-color 120ms ease, background-color 120ms ease, color 120ms ease;
    }

    .stButton > button:hover {
        color: var(--accent-strong);
        border-color: var(--accent);
        background: var(--surface-strong);
    }

    .stButton > button[kind="primary"] {
        color: #10201c;
        background: var(--accent);
        border-color: var(--accent);
        font-weight: 700;
    }

    .stButton > button[kind="primary"] p {
        color: #10201c !important;
        white-space: nowrap;
    }

    .stButton > button[kind="primary"]:hover {
        color: #0c1916;
        background: var(--accent-strong);
        border-color: var(--accent-strong);
    }

    .stButton > button[kind="primary"]:hover p {
        color: #0c1916 !important;
    }

    .stButton > button:focus-visible {
        outline: 2px solid var(--accent);
        outline-offset: 2px;
    }

    .stButton > button:disabled {
        color: #7e8b88;
        background: #20282b;
        border-color: var(--border);
        cursor: not-allowed;
    }

    .stButton > button:disabled p {
        color: #7e8b88 !important;
    }

    [data-testid="stFileUploader"] section,
    [data-testid="stExpander"] {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 10px;
    }

    [data-testid="stFileUploader"] section {
        padding: 1rem;
        background: #172023;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--surface);
        border-color: var(--border) !important;
        border-radius: 11px;
    }

    [data-testid="stChatMessage"] {
        margin: 0.65rem 0;
        padding: 1.1rem 1.25rem;
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 11px;
    }

    [data-testid="stChatInput"] {
        padding: 0.6rem;
        background: #1a2427;
        border: 1px solid #40514f;
        border-radius: 12px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.22);
    }

    [data-testid="stChatInput"] button {
        color: #10201c;
        background: var(--accent);
        border-radius: 8px;
    }

    .empty-state {
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        margin: 1rem 0 1.5rem;
        padding: 1.35rem 1.5rem;
        background: #192527;
        border: 1px solid #3b514c;
        border-left: 3px solid var(--accent);
        border-radius: 10px;
    }

    .empty-state .ui-icon {
        width: 1.5rem;
        height: 1.5rem;
        margin-top: 0.1rem;
        color: var(--accent);
    }

    .empty-state strong {
        color: var(--text);
        font-size: 1.05rem;
    }

    .empty-state p {
        margin: 0.3rem 0 0;
        color: var(--muted);
        line-height: 1.6;
    }

    .chat-heading {
        display: flex;
        align-items: center;
        gap: 0.9rem;
        margin: 0 0 1.4rem;
        padding: 0.25rem 0 1.2rem;
        border-bottom: 1px solid var(--border);
    }

    .chat-heading > .ui-icon {
        width: 1.7rem;
        height: 1.7rem;
        color: var(--accent);
    }

    .chat-heading h2 {
        margin: 0;
        color: var(--text);
        font-size: 1.45rem;
    }

    .chat-heading p {
        margin: 0.25rem 0 0;
        color: var(--muted);
        font-size: 0.96rem;
    }

    .project-card-title {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 0.75rem;
        color: var(--text);
        font-size: 1.2rem;
        font-weight: 650;
    }

    .project-card-title .ui-icon {
        color: var(--accent);
    }

    .document-row {
        display: flex;
        align-items: center;
        gap: 0.65rem;
        min-height: 3rem;
        padding: 0.6rem 0.85rem;
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 8px;
    }

    .document-row .ui-icon {
        color: var(--accent);
    }

    [data-testid="stAlert"] {
        color: var(--text);
        background: var(--surface-raised);
        border: 1px solid var(--border);
        border-radius: 9px;
    }

    [data-testid="stSpinner"] {
        color: var(--accent);
    }

    hr {
        border-color: var(--border);
    }

    @media (max-width: 640px) {
        .block-container {
            padding: 1.25rem 1rem 4rem;
        }

        .page-hero {
            gap: 0.8rem;
            margin-bottom: 1.4rem;
            padding: 1.2rem;
        }

        .page-hero h1 {
            font-size: 1.8rem;
        }

        .page-hero p {
            font-size: 0.98rem;
        }

        .page-hero .hero-icon {
            width: 2.5rem;
            height: 2.5rem;
            flex-basis: 2.5rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    st.markdown(
        f'<div class="brand-lockup">{icon_svg("library")}<span>Research Assistant</span></div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Powered by RAG + Hugging Face Inference"
    )

    st.divider()

if not is_hf_token_configured():
    st.warning("Configure HF_TOKEN in your environment or Streamlit secrets to enable answer generation.")

try:
    public_demo_mode = os.getenv(
        "PUBLIC_DEMO_MODE",
        st.secrets.get("PUBLIC_DEMO_MODE", "false")
    )
except Exception:
    public_demo_mode = os.getenv("PUBLIC_DEMO_MODE", "false")

public_demo_mode = str(public_demo_mode).lower() == "true"

if public_demo_mode and "workspace_id" not in st.session_state:
    st.session_state["workspace_id"] = uuid4().hex

workspace_id = st.session_state.get("workspace_id")

if "selected_project" in st.session_state:

    show_workspace(
        st.session_state[
            "selected_project"
        ],
        workspace_id
    )
else:

    show_projects(workspace_id)

