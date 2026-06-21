import streamlit as st

from components.rag_engine import(
    ask_project
)

def show_chat(
        project_name
):
    st.header(
        f"💬{project_name}"
    )

    if st.button(
        "← Back"
    ):
        
        del st.session_state[
            "chat_project"
        ]

        st.rerun()
    st.divider()

    if "messages" not in st.session_state:

        st.session_state.messages=[]
    
    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):
            
            st.markdown(
                message["content"]
            )

            if(
                message["role"]=="assistant"
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

        st.session_state.messages.append(
            {
                "role":"user",
                "content":query
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
                        sources
                    )
                    
        st.session_state.messages.append(
            {
                "role":"assistant",
                "content": answer,
                "sources": sources
            }
        )

        st.rerun()