import streamlit as st
import os
from html import escape

from modules.project_manager import (
    create_project,
    list_projects,
    get_project_paths,
    delete_project
)

from modules.index_manager import (
    load_index
)

from ui.components.icons import icon_svg


def show_projects(workspace_id):

    projects = list_projects(workspace_id)

    total_projects = len(projects)

    total_pdfs = 0

    for project in projects:

        pdfs_path, _ = get_project_paths(
            project,
            workspace_id
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

    st.markdown(
        f'<section class="page-hero"><div class="hero-icon">{icon_svg("library")}</div>'
        '<div><div class="eyebrow">Research library</div><h1>Research Assistant</h1>'
        '<p>Ask questions about your research documents and keep every paper organized by project.</p></div></section>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="section-heading">{icon_svg("folder")}<span>Projects</span></div>',
        unsafe_allow_html=True
    )

    # ---------------- Create Project ---------------- #

    with st.container(border=True):
        create_col, create_button_col = st.columns(
            [3, 1],
            vertical_alignment="bottom"
        )

        with create_col:
            new_project = st.text_input(
                "Project name",
                placeholder="Enter a project name"
            )

        with create_button_col:
            create_clicked = st.button(
                "Create project",
                type="primary",
                use_container_width=True
            )

    if create_clicked:
        new_project = new_project.strip()

        if not new_project:
            st.warning("Enter a project name.")

        elif new_project in projects:
            st.warning("Project already exists.")

        else:
            create_project(new_project, workspace_id)
            st.success(f"{new_project} created successfully.")
            st.rerun()

    # ---------------- Search ---------------- #

    st.markdown(
        f'<div class="section-heading">{icon_svg("search")}<span>Find a project</span></div>',
        unsafe_allow_html=True
    )

    with st.container(border=True):
        search = st.text_input(
            "Search projects",
            placeholder="Filter by project name"
        ).lower()

    filtered_projects = [

        project

        for project in projects

        if search in project.lower()

    ]

    if not filtered_projects:
        st.markdown(
            f'<div class="empty-state">{icon_svg("search")}<div><strong>No matching projects</strong>'
            '<p>Try another search, or create a project to get started.</p></div></div>',
            unsafe_allow_html=True
        )
        return

    # ---------------- Project Cards ---------------- #

    st.markdown(
        f'<div class="section-heading">{icon_svg("layers")}<span>Your workspaces</span></div>',
        unsafe_allow_html=True
    )

    with st.container(border=True):
        for project_index, project in enumerate(filtered_projects):

            pdfs_path, storage_path = get_project_paths(
                project,
                workspace_id
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

            st.markdown(
                f'<div class="project-card-title">{icon_svg("folder")}<span>{escape(project)}</span></div>',
                unsafe_allow_html=True
            )

            details_col, delete_col = st.columns(
                [4, 1],
                vertical_alignment="center"
            )

            with details_col:
                pdf_col, chunk_col = st.columns(2)
                with pdf_col:
                    st.caption(f"{pdf_count} PDFs")
                with chunk_col:
                    st.caption(f"{chunk_count} indexed chunks")

            with delete_col:
                if st.button(
                    "Delete",
                    key=f"delete_{project}"
                ):

                    delete_project(
                        project,
                        workspace_id
                    )

                    st.success(
                        f"{project} deleted."
                    )

                    st.rerun()

            if st.button(
                "Open Project",
                key=f"open_{project}",
                type="primary",
                use_container_width=True
            ):

                st.session_state[
                    "selected_project"
                ] = project

                st.rerun()

            if project_index < len(filtered_projects) - 1:
                st.divider()
