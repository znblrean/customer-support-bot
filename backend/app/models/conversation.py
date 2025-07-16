from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, JSON, Integer
from sqlalchemy.ext.declarative import declarative_base
from pgvector.sqlalchemy import Vector

Base = declarative_base()

class Conversation(Base):
    __tablename__ = 'conversations'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), index=True)
    session_id = Column(String(100), index=True)
    user_message = Column(Text)
    bot_response = Column(Text)
    sentiment = Column(String(20))
    intent = Column(String(50))
    embedding = Column(Vector(1536))  # برای OpenAI embeddings
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Conversation(user_id={self.user_id}, session_id={self.session_id})>"