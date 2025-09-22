import uuid
from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException
from groq import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from starlette.concurrency import run_in_threadpool

from chatbot import model
from ..RAG_with_history import invoke_rag_chain, create_retriever_from_document, create_retriever_from_a_collection_name
from ..database import engine
from ..model import Messages, Collections, Embeddings
from ..routers.auth import get_db
from ..schemas import RagChatRequest, RetrieverRequest,  CollectionsPutRequest
from .users import user_dependency


model.Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session , Depends(get_db)]

router = APIRouter(prefix="/RAGapp", tags=["Rag app"])


def put_user_id_for_message(session_id:str ,db:db_dependency,user:user_dependency):
    user_id = user.get("id")
    ai_message = db.query(Messages).filter(Messages.session_id == session_id).order_by(Messages.id.desc()).first()
    user_message =  db.query(Messages).filter(Messages.session_id == session_id).order_by(Messages.id.desc()).offset(1).first()
    ai_message.user_id = user_id
    user_message.user_id = user_id
    db.commit()

def put_user_id_for_collection(collection_name,user:user_dependency,db:db_dependency):
    user_id = user.get("id")
    model=db.query(Collections).filter(Collections.name == collection_name).first()
    model.user_id = user_id
    db.commit()




@router.put("/change_collection_by_name/{collection_name}",status_code=status.HTTP_204_NO_CONTENT)
async def change_collection_by_name(collection_name:str ,request:CollectionsPutRequest,user:user_dependency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    model = db.query(Collections).filter(Collections.user_id == user.get("id")).filter(Collections.name == collection_name).first()
    if model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cannot find the collection")
    try:
        model.name = request.name
        model.description = request.description
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error deleting collection: {str(e)}")

@router.delete("/delete_collection_by_name/{collection_name}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_collection_by_name(collection_name:str,user:user_dependency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    model = db.query(Collections).filter(Collections.user_id == user.get("id")).filter(Collections.name == collection_name).first()

    if model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cannot find the collection")
    embedding_model = db.query(Embeddings).filter(Embeddings.collection_id==model.id).first()
    try:
        db.delete(model)
        db.delete(embedding_model)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Error updating collection: {str(e)}")

@router.get("/user_get_collections",status_code=status.HTTP_200_OK)
async def get_user_collections(db:db_dependency,user:user_dependency):
    if user is None :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        model = db.query(Collections).filter(Collections.user_id == user.get("id")).all()
        collections = []
        for collection in model:
            collections.append(collection.name)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="error")
    return {"collection names": collections}



@router.post("/make_new_retriever", status_code=status.HTTP_201_CREATED)
async def make_new_retriever(request: RetrieverRequest, db: db_dependency, user: user_dependency):
    if user is None :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        create_retriever_from_document(request.splits , request.collection_name)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Cannot create retriever: {str(e)}")
    try:
        put_user_id_for_collection(request.collection_name, user, db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Cannot put user id for the collection: {str(e)}")


@router.post('/chat',status_code=status.HTTP_201_CREATED)
async def chat(rag_chat_request: RagChatRequest ,user: user_dependency,db : db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not authenticated")

    if not rag_chat_request.message:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail="Missing input")

    if not rag_chat_request.session_id:
        rag_chat_request.session_id = str(uuid.uuid4())

    try:
        retriever = create_retriever_from_a_collection_name(rag_chat_request.collection_name)
    except Exception as e :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Cannot find the collection: {str(e)}")

    try:
        response = invoke_rag_chain(
            rag_chat_request.message,
            rag_chat_request.session_id,
            retriever,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Cannot find the answer: {str(e)}")
    try:
        put_user_id_for_message(rag_chat_request.session_id, db, user)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Cannot put user id for the message: {str(e)}")

    return {"response": response,
            "session_id" : rag_chat_request.session_id}






