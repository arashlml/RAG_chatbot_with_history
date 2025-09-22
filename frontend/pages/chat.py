import uuid
from time import sleep

import streamlit as st

from .APIrequests import get_chat_history, invoke


def chatbot_page():
    st.header("Chatbot")
    if 'token' in st.session_state:
        if st.button("Start New Chat"):
            session_id = str(uuid.uuid4())
            st.success(f"New Chat created, your session id is {session_id}")
            st.session_state["session_ids"].append(session_id)
            sleep(1)
            st.rerun()

        options = st.session_state.get("session_ids", [])
        if not options:
            st.warning("No chats found. Start a new chat to begin.")
            return

        default_index = len(options) - 1 if options else 0
        session_id = st.selectbox("Select Chat History", options, index=default_index, key="chat_selector")

        history = get_chat_history(st.session_state["token"], session_id)
        if history:
            for msg in history:
                with st.chat_message(msg.get("type")):
                    st.markdown(msg.get("content"))

        if prompt := st.chat_input("Type your message..."):
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.spinner("Thinking..."):
                response = invoke(st.session_state["token"], session_id, prompt)
                if response:
                    with st.chat_message("assistant"):
                        st.markdown(response.get("content"))
                    st.rerun()
                else:
                    st.error("Failed to get a response from the chatbot.")

    else:
        st.error("You have not logged in")


if __name__ == "__main__":
    chatbot_page()