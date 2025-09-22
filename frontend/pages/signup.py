import streamlit as st


from .APIrequests import register, get_access_token, get_session_ids, get_user_collections


def signup_page():
    st.header("🆕 Sign Up")
    username = st.text_input("Choose a Username")
    first_name = st.text_input("Choose a First Name")
    last_name = st.text_input("Choose a Last Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        with st.spinner("Creating your account..."):
            if register(username, password, first_name, last_name, email):
                st.session_state["token"] = get_access_token(username, password)
                st.success("You're registered and logged in as {}".format(username))
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.current_page = "dashboard"
                st.session_state["session_ids"] = get_session_ids(st.session_state["token"]) or []
                st.session_state["collection_names"] = get_user_collections(st.session_state["token"]) or []
                st.toast("Account created successfully!")
                st.rerun()
            else:
                st.error("Something went wrong. Try again later")

if __name__ == "__main__":
    signup_page()