import streamlit as st

from modules.pdf_uploader import (
    upload_pdf
)

from modules.project_indexer import(
    rebuild_project_index
)


from pages.chat import(
    show_chat
)


def show_workspace(
        project_name
):
    st.header(
        project_name
    )

    if st.button(
        "← Back"
    ):
       del st.session_state[
           "selected_project"
       ]

       st.rerun()

    st.divider()

    st.subheader(
        "Upload PDF"
    ) 

    uploaded_file = st.file_uploader(
        "Choose PDF",
        type=["pdf"]
    )

    if(
        uploaded_file
        and
        st.button("Upload")
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
    st.divider()

    st.subheader(
        "Index"
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

    st.subheader(
        "Chat"
    )

    if st.button(
        "Ask Questions"
    ):
        
        st.session_state[
            "chat_project"
        ] = project_name

        st.session_state[
            "messages"
        ]= []


        st.rerun()

