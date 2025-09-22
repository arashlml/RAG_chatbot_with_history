import uuid
import streamlit as st
from .APIrequests import get_chat_history, rag_invoke



def rag_page():
    st.header("RAG chatbot with message history")
    col1, col2 ,col3 = st.columns(3)
    if 'token' in st.session_state:
        with col1:
            if st.button("Start New Chat"):
                with st.spinner("Processing..."):
                    session_id = str(uuid.uuid4())
                    st.session_state["session_ids"].append(session_id)
                    st.session_state["active_session"] = session_id
                    st.success(f"Chat created with session id {session_id}")
                    st.rerun()
        with col2:
            if st.button("dashboard"):
                st.session_state.current_page = "dashboard"
                st.rerun()
        with col3:
            if st.button("collections"):
                st.session_state.current_page = "collections"
                st.rerun()
        options = st.session_state.get("session_ids", [])
        if not options:
            st.warning("No chats found. Start a new chat to begin.")

        default_index = len(options) - 1 if options else 0
        session_id = st.selectbox("Select Chat History", options, index=default_index, key="chat_selector")

        collections_name = st.session_state.get("collection_names", [])
        if not collections_name:
            st.warning("No collection found")

        collection_name = st.selectbox("Select a collection", collections_name, key="collection_selector")

        history = get_chat_history(st.session_state["token"], session_id)
        if history:
            for msg in history:
                if isinstance(msg, dict) and "type" in msg and "content" in msg:
                    with st.chat_message(msg["type"]):
                        st.markdown(msg["content"])
                else:
                    st.warning("Invalid message format in chat history.")
        else:
            st.info("No chat history available for this session.")

        if prompt := st.chat_input("Type your message..."):
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.spinner("Thinking..."):
                try:
                    response = rag_invoke(st.session_state["token"], session_id, prompt, collection_name)
                    if response :
                        with st.chat_message("assistant"):
                            st.markdown(response.get("content"))
                        st.rerun()
                    else:
                        st.error("Invalid response from the chatbot.")
                except Exception as e:
                    st.error(f"Error during chatbot invocation: {str(e)}")
    else:
        st.error("You have not logged in")


if __name__ == "__main__":
    rag_page()