import logging
import os
import uuid

import psycopg
from dotenv import load_dotenv
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_groq import ChatGroq
from langchain_postgres import PostgresChatMessageHistory, PGVector


load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_TRACING_V2'] = "true"

llm = ChatGroq(model="openai/gpt-oss-120b")
embeddings=OllamaEmbeddings(base_url="http://ollama:11434",model="nomic-embed-text")
RAG_connection = "postgresql+psycopg://langchain:langchain@db:5432/langchain"
sync_connection= psycopg.connect("postgresql://langchain:langchain@db:5432/langchain")

def create_retriever_from_document(splits,collection_name):
    logging.debug(f"Creating retriever for collection: {collection_name}, splits: {len(splits)}")
    try:
        # Convert DocumentModel to langchain Document
        langchain_docs = [
            Document(page_content=doc.page_content, metadata=doc.metadata)
            for doc in splits
        ]
        logging.debug(f"Converted splits to langchain Documents: {len(langchain_docs)}")
        vector_store = PGVector.from_documents(
            documents=splits,
            embedding=embeddings,
            collection_name=collection_name,
            connection=RAG_connection,
            use_jsonb=True,
        )
        retriever = vector_store.as_retriever()
        logging.debug("Retriever created successfully")
    except Exception as e:
        logging.error(f"Error creating retriever: {str(e)}")
        raise
    return retriever

def create_retriever_from_a_collection_name(collection_name):
    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=collection_name,
        connection=RAG_connection,
        use_jsonb=True,
    )
    retriever = vector_store.as_retriever()
    return retriever



contextualize_q_system_prompt = (
    "Given a chat history and the latest user question"
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

# Answer question
system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
def create_rag_chain(retriever):
    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    return rag_chain

def get_session_history(session_id:str):
    chat_history = PostgresChatMessageHistory(
    'messages',
    session_id,
    sync_connection=sync_connection
)
    return chat_history

def invoke_rag_chain(user_input,session_id,retriever):
    rag_chain = create_rag_chain(retriever)
    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain, get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer"
    )
    config={"configurable": {"session_id":session_id}}
    response = conversational_rag_chain.invoke(
        {"input":user_input},
        config=config
    )
    return response