import os

from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_community.tools import ArxivQueryRun , WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper, ArxivAPIWrapper
from langchain.tools.retriever import create_retriever_tool
from dotenv import load_dotenv
from chatbot.RAG_with_history import create_retriever_from_a_collection_name
from chat_model import chat_model , get_session_history
from langchain import hub


load_dotenv()
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]="agent with tools"

api_wrapper_wiki = WikipediaAPIWrapper(top_k_results = 1,doc_content_chars_max=250)
wiki=WikipediaQueryRun(api_wrapper=api_wrapper_wiki)

api_wrapper_arxiv = ArxivAPIWrapper(top_k_results = 1,doc_content_chars_max=250)
arxiv = ArxivQueryRun(api_wrapper=api_wrapper_arxiv)

def create_retrievers_as_tool(collections_name):
    retrievers=[]
    for collection_name in collections_name:
        retrievers.append(create_retriever_tool(
            create_retriever_from_a_collection_name(collection_name),
            f"{collection_name}"
        ))
    return retrievers

tools = [wiki,arxiv]

prompt = hub.pull("hwchase17/openai-functions-agent")

def agent_invoke():
    agent = create_openai_tools_agent(chat_model,tools,prompt)
    agent_executor = AgentExecutor(agent=agent , tools= tools , verbose=True)






