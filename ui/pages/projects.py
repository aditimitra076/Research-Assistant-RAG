import streamlit as st

from modules.project_manager import (
    create_project,
    list_projects
)

def show_projects():
    st.header(
        "Projects"
    )

    new_project = st.text_input(
        "Project Name"
    )

    if st.button(
        "Create Project"
    ):
        if new_project:

            create_project(
                new_project
            )

            st.success(
                f"{new_project} created"
            )

            st.rerun()

    st.divider()

    projects = list_projects()

    if not projects:

        st.info(
            "No projects found"
        )

        return
    
    for project in projects:

        if st.button(
            f"📁 {project}",
            use_container_width=True
        ):
            
            st.session_state[
                "selected_project"
            ] = project

            st.rerun()