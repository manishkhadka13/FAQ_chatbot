from datetime import datetime,timezone
from sqlalchemy import Column, Integer, Text, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase
from pgvector.sqlalchemy import Vector

def utcnow():
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass

class FAQ(Base):
    __tablename__ = "faqs"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    category = Column(String(100), nullable=True)
    embedding = Column(Vector(384))
    created_at = Column(DateTime(timezone=True), default=utcnow)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)
    

class QueryLog(Base):
    __tablename__ = "query_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_query = Column(Text, nullable=False)
    matched_faq_id = Column(Integer, ForeignKey("faqs.id"), nullable=True)
    similarity = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utcnow)
    
    
