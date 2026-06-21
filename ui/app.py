import sys
import os


sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from pages.projects import show_projects

import streamlit as st

from pages.projects import(
    show_projects
)

from pages.workspace import(
    show_workspace
)


from pages.chat import(
    show_chat
)



st.set_page_config(
    page_title="Research Assistant",
    page_icon ="📚",
    layout="wide"
)

st.title(
    "📚 Research Assistant"
)



if "chat_project" in st.session_state:

    show_chat(
        st.session_state[
            "chat_project"
        ]
    )

elif "selected_project" in st.session_state:

    show_workspace(
        st.session_state[
            "selected_project"
        ]
    )
else:

    show_projects() 

