import streamlit as st


st.set_page_config(page_title="My App", page_icon="🏠", layout="wide")

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {display: none;}
    </style>
    """,
    unsafe_allow_html=True
)

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state.username = None
    st.session_state.current_page = "home"


def home_page():
    from pages.home import home_page
    home_page()

def login_page():
    from pages.login import login_page
    login_page()

def signup_page():
    from pages.signup import signup_page
    signup_page()

def dashboard_page():
    from pages.dashboard import dashboard_page
    dashboard_page()
def chat_page():
    from pages.chat import chatbot_page
    chatbot_page()

def rag_page():
    from pages.rag import rag_page
    rag_page()

def collections_page():
    from pages.collections import collections_page
    collections_page()

page_map = {
    "home": home_page,
    "login": login_page,
    "sign_up": signup_page,
    "dashboard": dashboard_page,
    "chat": chat_page,
    "rag": rag_page,
    "collections": collections_page,
}

if st.session_state.current_page in ["dashboard", "chatbot_page"] and not st.session_state.logged_in:
    st.session_state.current_page = "login"

page_map.get(st.session_state.current_page, home_page)()


















