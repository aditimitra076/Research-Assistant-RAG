import streamlit as st

from components.rag_engine import(
    ask_project
)


def show_chat(
        project_name
):

    st.markdown(
        f"## 💬 {project_name}"
    )

    if st.button(
        "← Back",
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
                    "Sources"
                ):

                    for source in message[
                        "sources"
                    ]:
                        st.write(
                            source
                        )

    query = st.chat_input(
        "Ask anything..."
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

        answer, sources = ask_project(
            project_name,
            query
        )

        with st.chat_message(
            "assistant"
        ):

            st.markdown(
                answer
            )

            with st.expander(
                "Sources"
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