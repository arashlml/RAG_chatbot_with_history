import streamlit as st

def dashboard_page():

    st.title("Dashboard")
    st.write(f"Welcome, {st.session_state.username}! This is your dashboard.")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Go to Profile"):
            st.session_state.current_page = "profile"
            st.rerun()
        if st.button("Go to Collection"):
            st.session_state.current_page = "collections"
            st.rerun()
    with col2:
        if st.button("Chatbot"):
            st.session_state.current_page = "chat"
            st.rerun()
        if st.button("Rag chatbot with history"):
            st.session_state.current_page = "rag"
            st.rerun()
    with col3:
        if st.button("Log Out"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.current_page = "home"
            st.rerun()


if __name__ == "__main__":
    dashboard_page()