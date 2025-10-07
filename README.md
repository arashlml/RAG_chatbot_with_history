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
The `.env` file is located in the `chatbot` folder of the project. You need to add the following environment variables to configure the LangChain and Grok APIs:

```env
LANGCHAIN_API_KEY=your_langchain_api_key_here
LANGCHAIN_TRACING_V2=true
GROQ_API_KEY=your_groq_api_key_here
```

**Where to Find the API Keys**:
- **LANGCHAIN_API_KEY**: Sign up at [LangChain](https://www.langchain.com/) and navigate to your account settings to generate an API key. Copy the key and replace `your_langchain_api_key_here` with it.
- **GROQ_API_KEY**: Register at [Groq](https://groq.com/) to obtain a Grok API key. After logging in, find the API key in your account dashboard and replace `your_groq_api_key_here` with it.

Ensure the `.env` file is saved in the `chatbot` folder before proceeding.
### 2. Start the Application

Run the app using Docker Compose:

```bash
docker-compose up --build
```

**Troubleshooting Network Issues**:
If you encounter an **Error 404** in the container when accessing APIs, try using a VPN. Preferably, connect to a server in a country not under UN sanctions to ensure stable connectivity. 😄🚀😂

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



