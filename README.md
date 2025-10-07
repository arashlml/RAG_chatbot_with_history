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
### 1. first complete the .env file 
### 2. Start the Application

Run the app using Docker Compose:

```bash
docker-compose up --build
```
Once the services are running, open your browser and go to:

```arduino
http://localhost:5000
```
### 3. Create an Account
Users must create an account to start interacting with the chatbot.

### 4. Using the Chatbot

Standard Chatbot: Ask questions without using RAG.

Chatbot with RAG:

Create a collection by uploading a PDF (must be in English).

Give a meaningful name to the collection.

Go to the RAG section, select the collection by name, and choose the conversation history you want to continue.

---

## Wishing You Success! 🎉

I hope you enjoy using this chatbot and make the most out of its features. May your experiments with RAG, LangChain, and conversation history be insightful and fun. Good luck! 🚀

