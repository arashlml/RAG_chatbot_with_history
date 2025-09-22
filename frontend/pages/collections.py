
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


from .APIrequests import make_new_retriever

def create_chucks_of_docs(uploaded_file):
    documents=[]
    temppdf = f"frontend/temp.pdf"
    with open(temppdf, "wb") as file:
        file.write(uploaded_file.getvalue())
        file_name = uploaded_file.name
    loader = PyPDFLoader(temppdf)

    docs = loader.load()
    if docs is not None:
        documents.extend(docs)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=500)
        splits = text_splitter.split_documents(documents)
    else:
        raise Exception(f"pypdf Could not load {temppdf}")
    return splits



def collections_page():
    st.header("Collections")
    st.write("Your collections:")
    for collection in st.session_state["collection_names"]:
        st.write("-", collection)
    uploaded_file = st.file_uploader("Choose a PDF", type="pdf")
    collection_name = st.text_input("Enter Collection Name")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button('Make a new collection') and uploaded_file and collection_name:
            try:
                with st.spinner("Processing..."):
                    splits = create_chucks_of_docs(uploaded_file)
                    if splits is None:
                        raise Exception(f"Could not create {collection_name}")
                    else:
                        make_new_retriever(st.session_state['token'], collection_name, splits)
                        st.session_state["collection_names"].append(collection_name)
                        st.success("Your collection has been created with name : " + collection_name)
                        st.rerun()
            except Exception as e:
                st.error(e)

    with col2:
        if st.button("Go back"):
            st.session_state.current_page = "dashboard"
            st.rerun()
    with col3:
        if st.button("RAG chatbot"):
            st.session_state.current_page = "rag"
            st.rerun()



if __name__ == "__main__":
    collections_page()