import streamlit as st

def home_page():
    st.title("Home Page")
    st.write("""
This project is a full-stack web application designed to provide users with an interactive chatbot experience. The application is built using a modern Python technology stack, featuring a decoupled frontend and backend architecture to ensure scalability and maintainability.

**Backend Architecture:**

The backend is a robust API service developed using the FastAPI framework. This choice provides high performance for I/O-bound operations, automatic interactive API documentation (via Swagger UI and ReDoc), and a clean, modern syntax for defining API endpoints. The backend is responsible for several core functionalities:

*   **User Authentication and Management:** Secure user registration, login, and profile management are handled through dedicated API endpoints. The system includes authentication logic to protect routes and ensure that only authorized users can access their data and the chatbot features.
*   **Chatbot API:** The core of the application is the chat model API. It exposes endpoints that the frontend can call to send user messages and receive responses from the chatbot. This modular approach allows the chat model itself to be updated or replaced with minimal impact on the rest of the application.
*   **Database Interaction:** The application uses a database (the specific type is managed via `database.py`) to persist user data, chat history, and other relevant information. This ensures that user sessions and conversations can be maintained over time.
*   **Modular Routers:** The API is organized into logical modules (routers) for different concerns, such as authentication (`auth.py`), user operations (`users.py`), and the chat model (`chat_model_api.py`), making the codebase easy to navigate and extend.

**Frontend Architecture:**

The frontend is a multi-page web application, likely built with a framework like Streamlit. This allows for the rapid development of interactive and data-centric user interfaces purely in Python. The frontend is structured into several distinct pages:

*   **Home:** A landing page that provides an overview of the application.
*   **Login/Signup:** Standard pages for user account creation and authentication.
*   **Chat:** The main interface where users can interact with the chatbot.
*   **Profile:** A page for users to view and manage their profile information.
*   **Dashboard:** A potential area for displaying usage statistics or other relevant user data.

The frontend communicates with the backend via HTTP requests to the FastAPI endpoints, creating a seamless and responsive user experience. This separation of concerns between the frontend and backend is a key architectural feature, allowing for independent development, deployment, and scaling of each component.
    """)

    st.write("To start using the chat, please sign in or create an account.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sign in",key="signin"):
            st.session_state.current_page = "login"
            st.rerun()
    with col2:
        if st.button("Sign Up",key="signup"):
            st.session_state.current_page = "sign_up"
            st.rerun()


if __name__ == "__main__":
    home_page()