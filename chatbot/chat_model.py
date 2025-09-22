import os
import uuid

import psycopg
from dotenv import load_dotenv
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_groq import ChatGroq
from langchain_postgres import PostgresChatMessageHistory
from .database import SQLALCHEMY_DATABASE_URI
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_TRACING_V2'] = "true"


chat_model = ChatGroq(model="openai/gpt-oss-120b")

session_id = str(uuid.uuid4())
sync_connection = psycopg.connect("postgresql://langchain:langchain@db:5432/langchain")

def get_session_history(session_id:str):
    chat_history = PostgresChatMessageHistory(
    'messages',
    session_id,
    sync_connection=sync_connection
)
    return chat_history

with_message_history = RunnableWithMessageHistory(
    chat_model,
    get_session_history
)


def model_invoke(model ,message ,session_id ):
    config = {"configurable": {"session_id": session_id}}
    response = model.invoke({"input": message}, config=config)
    return response
