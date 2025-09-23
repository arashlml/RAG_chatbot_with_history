# RAG Chatbot with History

A web-based chatbot application built using **FastAPI**, **Streamlit**, **LangChain**, and **PostgreSQL**, with optional **Retrieval-Augmented Generation (RAG)** for answering questions based on uploaded documents. The app also supports maintaining conversation history.

---

## Features

- **FastAPI Backend** for API endpoints and RAG logic  
- **Streamlit Frontend** for an interactive and user-friendly interface  
- **LangChain Integration** for RAG-based question answering  
- **PostgreSQL Database** for storing user accounts, conversation history, and document collections  
- **Conversation History**: Chatbot can continue previous conversations  
- **RAG Support**: Upload PDFs to create collections and query them using the chatbot  

---

## How to Use

### 1. Start the Application

Run the app using Docker Compose:

```bash
docker-compose up --build

