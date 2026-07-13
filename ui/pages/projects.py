import streamlit as st
import os

from modules.project_manager import (
    create_project,
    list_projects,
    get_project_paths,
    delete_project
)

from modules.index_manager import (
    load_index
)


def show_projects():

    projects = list_projects()

    total_projects = len(projects)

    total_pdfs = 0

    for project in projects:

        pdfs_path, _ = get_project_paths(
            project
        )

        if os.path.exists(pdfs_path):

            total_pdfs += len(
                [
                    file
                    for file in os.listdir(pdfs_path)
                    if file.endswith(".pdf")
                ]
            )

    # ---------------- Sidebar ---------------- #

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

    # ---------------- Header ---------------- #

    st.title(
        "📚 Projects"
    )

    st.caption(
        "Manage your Research Assistant workspaces."
    )

    # ---------------- Create Project ---------------- #

    new_project = st.text_input(
        "Project Name"
    )

    if st.button(
        "Create Project"
    ):

        new_project = new_project.strip()

        if not new_project:

            st.warning(
                "Enter a project name."
            )

        elif new_project in projects:

            st.warning(
                "Project already exists."
            )

        else:

            create_project(
                new_project
            )

            st.success(
                f"{new_project} created successfully."
            )

            st.rerun()

    st.divider()

    # ---------------- Search ---------------- #

    search = st.text_input(
        "🔍 Search Projects"
    ).lower()

    filtered_projects = [

        project

        for project in projects

        if search in project.lower()

    ]

    if not filtered_projects:

        st.info(
            "No matching projects found."
        )

        return

    # ---------------- Project Cards ---------------- #

    for project in filtered_projects:

        pdfs_path, storage_path = get_project_paths(
            project
        )

        pdf_count = 0

        chunk_count = 0

        if os.path.exists(
            pdfs_path
        ):

            pdf_count = len(
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

        _, chunks = load_index(
            storage_path
        )

        if chunks:

            chunk_count = len(
                chunks
            )

        with st.container():

            st.markdown(
                f"### 📁 {project}"
            )

            col1, col2, col3 = st.columns(
                [2, 2, 1]
            )

            with col1:

                st.caption(
                    f"📄 PDFs: {pdf_count}"
                )

            with col2:

                st.caption(
                    f"🧩 Chunks: {chunk_count}"
                )

            with col3:

                if st.button(
                    "🗑",
                    key=f"delete_{project}"
                ):

                    delete_project(
                        project
                    )

                    st.success(
                        f"{project} deleted."
                    )

                    st.rerun()

            if st.button(
                "Open Project",
                key=f"open_{project}"
            ):

                st.session_state[
                    "selected_project"
                ] = project

                st.rerun()

            st.divider()