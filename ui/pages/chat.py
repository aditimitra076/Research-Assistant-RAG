import streamlit as st
from html import escape
from modules.generator import format_generation_error



from components.rag_engine import(
    ask_project
)

from ui.components.icons import icon_svg


def show_chat(
    project_name,
    workspace_id
):

    st.markdown(
        f'<div class="chat-heading">{icon_svg("message")}<div><h2>{escape(project_name)}</h2>'
        '<p>Ask a question grounded in this project’s documents.</p></div></div>',
        unsafe_allow_html=True
    )

    if st.button(
        "Back to workspace",
        key="chat_back"
    ):

        st.session_state[
            "chat_mode"
        ] = False

        st.rerun()

    st.divider()

    if (
        "project_chats"
        not in st.session_state
    ):
        st.session_state[
            "project_chats"
        ] = {}

    if (
        project_name
        not in st.session_state[
            "project_chats"
        ]
    ):
        st.session_state[
            "project_chats"
        ][project_name] = []

    messages = st.session_state[
        "project_chats"
    ][project_name]

    if not messages:
        st.markdown(
            f'<div class="empty-state">{icon_svg("message")}<div><strong>Your research conversation starts here</strong>'
            '<p>Ask about the documents in this project. Answers will include retrieved sources when available.</p></div></div>',
            unsafe_allow_html=True
        )

    for message in messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )

            if (
                message["role"] == "assistant"
                and
                "sources" in message
            ):

                with st.expander(
                    "Retrieved sources"
                ):

                    for source in message[
                        "sources"
                    ]:
                        st.write(
                            source
                        )

    query = st.chat_input(
        "Ask a question about your documents..."
    )

    if query:

        messages.append(
            {
                "role": "user",
                "content": query
            }
        )

        with st.chat_message(
            "user"
        ):
            st.markdown(
                query
            )

        try:
            with st.spinner("Retrieving relevant passages and generating an answer..."):
                answer, sources = ask_project(
                    project_name,
                    query,
                    workspace_id
                )
        except Exception as error:
            answer = format_generation_error(error)
            sources = []

        with st.chat_message(
            "assistant"
        ):

            st.markdown(
                answer
            )

            with st.expander(
                "Retrieved sources"
            ):

                for source in sources:
                    st.write(
                        source
                    )

        messages.append(
            {
                "role": "assistant",
                "content": answer,
                "sources": sources
            }
        )

        st.rerun()