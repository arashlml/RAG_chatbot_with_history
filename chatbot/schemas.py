from typing import Dict, Any, List

from pydantic import BaseModel


class ChatRequest(BaseModel):
    session_id: str
    message:str

class CreateUserRequest(BaseModel):
    username: str
    password: str
    email: str
    first_name: str
    last_name: str
    role: str

class UserVerification(BaseModel):
    username: str
    password: str
    new_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class SessionID(BaseModel):
    session_id: str

class ID(BaseModel):
    id: int

class RagChatRequest(BaseModel):
    session_id: str
    message: str
    collection_name:str

class DocumentModel(BaseModel):
    page_content: str
    metadata: Dict[str, Any]

class RetrieverRequest(BaseModel):
    splits: List[DocumentModel]
    collection_name: str

class CollectionsPutRequest(BaseModel):
    name: str
    description: str