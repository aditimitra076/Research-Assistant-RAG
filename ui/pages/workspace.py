import streamlit as st

import os
import tempfile
from html import escape

from modules.project_manager import(
    get_project_paths
)

from modules.pdf_uploader import (
    upload_pdf
)

from modules.project_indexer import(
    rebuild_project_index
)

from modules.generator import format_generation_error

from pages.chat import(
    show_chat
)

from modules.index_manager import(
    load_index
)

from ui.components.rag_engine import(
    summarize_project,
    research_gaps_project
)

from ui.components.icons import icon_svg

def show_workspace(
    project_name,
    workspace_id
):
    st.markdown(
        f'<section class="page-hero"><div class="hero-icon">{icon_svg("folder")}</div>'
        f'<div><div class="eyebrow">Research workspace</div><h1>{escape(project_name)}</h1>'
        '<p>Manage papers, refresh the knowledge base, and explore document-grounded answers.</p></div></section>',
        unsafe_allow_html=True
    )

    pdfs_path, storage_path = get_project_paths(
        project_name,
        workspace_id
    )

    pdf_count = 0
    chunk_count =0


    if os.path.exists(
        pdfs_path
    ):
        
        pdf_count =len(
            [
                file
                for file in os.listdir(
                    pdfs_path
                )

                if file.endswith(".pdf")
            ]
        )

    index, chunks = load_index(
        storage_path
    )

    if chunks:
        chunk_count = len(
            chunks
        )

    col1, col2, col3 = st.columns(3)
    

    with col1:
        st.metric(
            "PDFs",
            pdf_count
        )
    with col2:
        st.metric(
            "Chunks",
            chunk_count
        )

    with col3:
        st.metric(
            "Indexed",
            "Yes" if index else "No"
        )
    
    st.divider()

    if st.button(
        "Back to projects"
    ):
       if "selected_project" in st.session_state:
           del st.session_state[
               "selected_project"
           ]

       if "chat_mode" in st.session_state:
           del st.session_state[
               "chat_mode"
           ]

       st.rerun()

    st.divider()

    upload_col, knowledge_col = st.columns(2, gap="large")

    with upload_col:
        with st.container(border=True):
            st.markdown(
                f'<div class="section-heading">{icon_svg("upload")}<span>Add a research paper</span></div>',
                unsafe_allow_html=True
            )

            uploaded_file = st.file_uploader(
                "Choose a PDF",
                type=["pdf"],
                max_upload_size=20
            )

            if uploaded_file and st.button("Upload PDF", type="primary"):
                temp_path = None
                try:
                    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
                        temp_file.write(uploaded_file.getbuffer())
                        temp_path = temp_file.name

                    with st.spinner("Saving the PDF and building its index..."):
                        upload_pdf(temp_path, project_name, workspace_id)
                    st.success("PDF uploaded and indexed successfully.")
                except Exception:
                    st.error("The PDF could not be processed. Try a valid, text-based PDF and upload it again.")
                finally:
                    if temp_path and os.path.exists(temp_path):
                        try:
                            os.remove(temp_path)
                        except OSError:
                            pass

    with knowledge_col:
        with st.container(border=True):
            st.markdown(
                f'<div class="section-heading">{icon_svg("layers")}<span>Knowledge base</span></div>',
                unsafe_allow_html=True
            )

            if st.button("Rebuild Index"):
                success = rebuild_project_index(project_name, workspace_id)

                if success:
                    st.success("Index rebuilt")
                else:
                    st.warning("No PDFs uploaded in this project.")

            st.markdown(
                f'<div class="section-heading">{icon_svg("file")}<span>Paper summary</span></div>',
                unsafe_allow_html=True
            )

            if st.button("Generate Summary"):
                try:
                    with st.spinner("Generating summary..."):
                        summary = summarize_project(project_name, workspace_id)

                    if summary:
                        st.session_state["paper_summary"] = summary
                    else:
                        st.error("The summary could not be generated. Check the inference configuration and try again.")
                except Exception as error:
                    st.error(format_generation_error(error))

            if "paper_summary" in st.session_state:
                st.markdown(st.session_state["paper_summary"])

                st.markdown(
                    f'<div class="section-heading">{icon_svg("search")}<span>Research gap finder</span></div>',
                    unsafe_allow_html=True
                )

                if st.button("Find Research Gaps"):
                    try:
                        with st.spinner("Analyzing paper..."):
                            gaps = research_gaps_project(project_name, workspace_id)

                        if gaps:
                            st.session_state["research_gaps"] = gaps
                        else:
                            st.error("Research gaps could not be generated. Check the inference configuration and try again.")
                    except Exception as error:
                        st.error(format_generation_error(error))

                if "research_gaps" in st.session_state:
                    st.markdown(st.session_state["research_gaps"])

    st.markdown(
        f'<div class="section-heading">{icon_svg("file")}<span>Documents</span></div>',
        unsafe_allow_html=True
    )

    pdfs_path, _ = get_project_paths(
        project_name,
        workspace_id
    )

    pdf_files = []

    if os.path.exists(
        pdfs_path
    ):
        
        pdf_files = [
            file
            for file in os.listdir(
                pdfs_path
            )
            if file.endswith(
                ".pdf"
            )
        ]
    if not pdf_files:
        st.info(
            "No PDFs uploaded yet."
        )
    else:
        for pdf in pdf_files:
            st.markdown(
                f'<div class="document-row">{icon_svg("file")}<span>{escape(pdf)}</span></div>',
                unsafe_allow_html=True
            )

    st.markdown(
        f'<div class="section-heading">{icon_svg("message")}<span>Chat</span></div>',
        unsafe_allow_html=True
    )

    if st.button(
        "Open chat"
    ):

        st.session_state[
            "chat_mode"
        ] = True

        st.rerun()

    if st.session_state.get(
        "chat_mode",
        False
    ):
        
        show_chat(
            project_name,
            workspace_id
        )
