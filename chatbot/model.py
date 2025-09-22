import uuid


from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql.functions import func

from chatbot.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON ,UUID


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)

class Messages(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True )
    session_id = Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4)
    message = Column(JSONB, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class Collections(Base):
    __tablename__ = "langchain_pg_collection"
    uuid = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True )
    name = Column(String)
    cmetadata = Column(JSON)

class Embeddings(Base):
    __tablename__ = "langchain_pg_embedding"
    id = Column(String, primary_key=True)
    collection_id = Column(UUID(as_uuid=True), ForeignKey("langchain_pg_collection.uuid", ondelete="CASCADE"),nullable=False)
    embedding = Column(Vector(768))
    document = Column(String)
    cmetadata = Column(JSONB)


