import streamlit as st

import os

from modules.project_manager import(
    get_project_paths
)

from modules.pdf_uploader import (
    upload_pdf
)

from modules.project_indexer import(
    rebuild_project_index
)


from pages.chat import(
    show_chat
)

from modules.index_manager import(
    load_index
)



def show_workspace(
        project_name
):
    st.markdown(
        f"## 📁{project_name}"
    )

    st.caption(
        "Research Workspace"
    )

    pdfs_path, storage_path = get_project_paths(
        project_name
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
        "← Back"
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

    

    col1, col2 = st.columns(2)

    with col1 :

        st.markdown(
        "###📄Upload Document"
    ) 

    uploaded_file = st.file_uploader(
        "Choose PDF",
        type=["pdf"]
    )

    if(
        uploaded_file
        and
        st.button(
            "Upload PDF"
        )
    ):
        
        temp_path = uploaded_file.name

        with open(
            temp_path,
            "wb"
        ) as file:
            
            file.write(
                uploaded_file.getbuffer()
            )
        upload_pdf(
            temp_path,
            project_name
        )

        st.success(
            "PDF uploaded successfully"
        )
    
    with col2:

        st.markdown(
            "###⚡Knowledge Base"
        )


        if st.button(
            "Rebuild Index"
        ):
        
            success = rebuild_project_index(
                project_name
            )

            if success:

                st.success(
                    "Index rebuilt"
                )
            else:
                st.warning(
                    "No PDFs uploaded in this project."
                )

    st.divider()

    st.markdown(
        "### 📚 Documents"
    )

    pdfs_path, _ = get_project_paths(
        project_name
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

            col1, col2 = st.columns(
                [8,1]
            )

            with col1:
                st.write(
                    f"📄{pdf}"
                )
            with col2:
                st.caption(
                    "PDF"
                )

    st.markdown(
        "###💬Chat"
    )

    if st.button(
        "Open Chat"
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
            project_name
        )
