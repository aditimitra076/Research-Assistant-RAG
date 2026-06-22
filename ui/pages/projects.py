import streamlit as st
import os

from modules.project_manager import (
    create_project,
    list_projects,
    get_project_paths
)

def show_projects():

    projects = list_projects()

    total_projects = len(
        projects
    )

    total_pdfs = 0

    
    for project in projects:
        pdfs_path, _ = get_project_paths(
            project
        )

        if os.path.exists(
            pdfs_path
        ):
            total_pdfs+=len(
                [
                    file
                    for file in os.listdir(
                        pdfs_path
                    )

                    if file.endswith(
                        ".pdf"
                    )
                ]
            )


    with st.sidebar:
        st.subheader(
            "Statistics"
        )

        st.metric(
            "Projects",
            total_projects
        )

        st.metric(
            "PDFs",
            total_pdfs
        )

        st.divider()

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