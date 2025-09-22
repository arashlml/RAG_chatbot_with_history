
from fastapi import FastAPI
from . import model
from .routers import auth, chat_model_api, users, RAG_API
from .database import engine

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(chat_model_api.router)
app.include_router(users.router)
app.include_router(RAG_API.router)





