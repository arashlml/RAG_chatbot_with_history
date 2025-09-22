import streamlit as st
from .APIrequests import get_access_token, get_session_ids, get_user_collections


def login_page():
    st.header("Sign In")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login",key="Login"):
        with st.spinner("Signing in..."):
            token = get_access_token(username, password)
            if token:
                st.session_state["token"] = token
                st.success("Logged in as {}".format(username))
                st.session_state.current_page = "dashboard"
                st.session_state["username"] = username
                st.session_state.logged_in = True
                st.session_state["session_ids"] = get_session_ids(st.session_state["token"]) or []
                st.session_state["collection_names"]=get_user_collections(st.session_state["token"]) or []
                st.toast(f"Welcome back, {username}!")
                st.rerun()
            else:
                st.error("Wrong username or password")

if __name__ == "__main__":
    login_page()
