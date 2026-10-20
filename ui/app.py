import os
import sys
from uuid import uuid4

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

ui_path = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(ui_path)

for import_path in (ui_path, project_root):
    if import_path not in sys.path:
        sys.path.insert(0, import_path)

from pages.projects import show_projects
from pages.workspace import show_workspace
from ui.components.icons import icon_svg
from modules.generator import is_api_key_configured

st.set_page_config(page_title="Research Assistant", layout="wide")
st.markdown(
    """
    <style>
    :root { color-scheme: dark; --page: #111719; --surface: #192124;
      --raised: #202a2e; --border: #354448; --text: #edf3f1;
      --muted: #aab8b5; --accent: #78d6bd; }
    [data-testid="stAppViewContainer"] { background: var(--page); color: var(--text); }
    [data-testid="stHeader"] { background: var(--page); }
    .block-container { max-width: 1120px; padding: 2.25rem 2.5rem 5rem; }
    [data-testid="stSidebar"] { background: #151d20; border-right: 1px solid var(--border); }
    .brand-lockup { display:flex; align-items:center; gap:.7rem; color:var(--text); font-size:1.15rem; font-weight:700; }
    .ui-icon { display:inline-block; width:1.2rem; height:1.2rem; flex:0 0 auto; vertical-align:middle; }
    .page-hero { display:flex; gap:1rem; margin-bottom:1.5rem; padding:1.5rem;
      background:#192527; border:1px solid var(--border); border-left:4px solid var(--accent); border-radius:10px; }
    .page-hero .hero-icon,.section-heading .ui-icon,.chat-heading>.ui-icon { color:var(--accent); }
    .page-hero h1,.chat-heading h2 { color:var(--text); }
    .page-hero p,.chat-heading p,[data-testid="stMarkdownContainer"] p { color:var(--muted); }
    .section-heading { display:flex; align-items:center; gap:.65rem; margin:.8rem 0; color:var(--text); font-size:1.15rem; font-weight:650; }
    .document-row,.empty-state,[data-testid="stChatMessage"] { display:flex; gap:.8rem; padding:1rem; margin:.6rem 0; background:var(--surface); border:1px solid var(--border); border-radius:8px; }
    .stButton>button { min-height:2.7rem; color:var(--text); background:var(--raised); border:1px solid var(--border); border-radius:8px; }
    [data-testid="stVerticalBlockBorderWrapper"],[data-testid="stExpander"],[data-testid="stFileUploader"] section { background:var(--surface); border-color:var(--border); border-radius:8px; }
    hr { border-color:var(--border); }
    @media(max-width:640px) { .block-container { padding:1.2rem 1rem 4rem; } .page-hero { padding:1rem; } }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown(
        f'<div class="brand-lockup">{icon_svg("library")}<span>Research Assistant</span></div>',
        unsafe_allow_html=True,
    )
    st.caption("Powered by RAG + Gemini")
    st.divider()

if not is_api_key_configured():
    st.warning("Add your GEMINI_API_KEY to the .env file and restart Streamlit to enable generation. Get a free key at https://aistudio.google.com/apikey")

try:
    public_demo_mode = os.getenv(
        "PUBLIC_DEMO_MODE",
        st.secrets.get("PUBLIC_DEMO_MODE", "false"),
    )
except Exception:
    public_demo_mode = os.getenv("PUBLIC_DEMO_MODE", "false")

public_demo_mode = str(public_demo_mode).lower() == "true"

if public_demo_mode and "workspace_id" not in st.session_state:
    st.session_state["workspace_id"] = uuid4().hex

workspace_id = st.session_state.get("workspace_id")

if "selected_project" in st.session_state:
    show_workspace(st.session_state["selected_project"], workspace_id)
else:
    show_projects(workspace_id)
