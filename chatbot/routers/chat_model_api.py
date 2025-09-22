import uuid
from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from chatbot import model
from ..chat_model import get_session_history, with_message_history, model_invoke
from ..database import engine
from ..model import Messages
from ..routers.auth import get_db
from ..schemas import ChatRequest, SessionID, ID
from .users import user_dependency


model.Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session , Depends(get_db)]

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

@router.get("/chat_history/sessionID/", status_code=status.HTTP_200_OK)
async def get_session_chat_history(session_id : str,user:user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    chat_history = get_session_history(session_id)
    return chat_history.messages

def find_session_ids(user:user_dependency,db:db_dependency):
    id = user.get("id")
    model = db.query(Messages).filter(Messages.user_id == id).all()
    session_ids = set()
    for message in model:
        session_ids.add(message.session_id)
    return list(session_ids)

@router.get("/chat_history/user/", status_code=status.HTTP_200_OK)
async def get_session_id_by_user_id(db:db_dependency, user:user_dependency):
    if user is None :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="unauthorized")
    session_ids=find_session_ids(user,db)
    return {"session_ids" : session_ids}

def put_user_id(session_id:str ,db:db_dependency,user:user_dependency):
    user_id = user.get("id")
    ai_message = db.query(Messages).filter(Messages.session_id == session_id).order_by(Messages.id.desc()).first()
    user_message =  db.query(Messages).filter(Messages.session_id == session_id).order_by(Messages.id.desc()).offset(1).first()
    ai_message.user_id = user_id
    user_message.user_id = user_id
    db.commit()

@router.post('/chat',status_code=status.HTTP_201_CREATED)
async def chat(chat_request: ChatRequest,user: user_dependency,db : db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if not chat_request.message :
        return {"error": "Missing input"}
    if not chat_request.session_id :
        chat_request.session_id = str(uuid.uuid4())
    response = model_invoke(
        with_message_history,
        chat_request.message,
        chat_request.session_id
    )
    put_user_id(chat_request.session_id ,db,user)

    return {"response": response,
            "session_id" : chat_request.session_id}





