"""Database Models"""
from sqlalchemy import Column, String, DateTime, Text, JSON, Integer, Boolean, Float
from sqlalchemy.sql import func
from app.db.database import Base
import uuid


def generate_uuid():
    """Generate unique identifier"""
    return str(uuid.uuid4())


class EmailRecord(Base):
    """Email record model for storing processed emails"""
    __tablename__ = "emails"
    
    # Primary key
    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    
    # Gmail metadata
    gmail_id = Column(String, unique=True, index=True, nullable=False)
    thread_id = Column(String, index=True)
    
    # Email basic info
    sender = Column(String, index=True, nullable=False)
    recipient = Column(String)
    subject = Column(String, nullable=False)
    timestamp = Column(DateTime, index=True, nullable=False)
    
    # AI-processed content
    category = Column(String, index=True)  # Diagnostic Report, Insurance Claim, etc.
    priority = Column(String, index=True)  # high, medium, low
    summary = Column(Text)
    content = Column(Text)
    
    # Extracted entities (JSON)
    entities = Column(JSON)  # {patient_name, doctor, department, amount, etc.}
    
    # Attachments info
    attachments = Column(JSON)  # [{filename, type, size, content_summary}]
    
    # Processing status
    status = Column(String, default="unread")  # unread, pending, processed, archived
    processed_at = Column(DateTime)
    
    # Confidence scores
    confidence_score = Column(Float)  # AI categorization confidence
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Soft delete
    is_deleted = Column(Boolean, default=False)


class User(Base):
    """User model for authentication"""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    
    # Gmail OAuth tokens
    gmail_access_token = Column(Text)
    gmail_refresh_token = Column(Text)
    gmail_token_expiry = Column(DateTime)
    
    # User status
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    last_login = Column(DateTime)


class QueryHistory(Base):
    """Store user query history for analytics"""
    __tablename__ = "query_history"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, index=True)
    query_text = Column(Text, nullable=False)
    results_count = Column(Integer)
    execution_time = Column(Float)  # in seconds
    created_at = Column(DateTime, server_default=func.now())


class EmailEmbedding(Base):
    """Store email embeddings for RAG queries"""
    __tablename__ = "email_embeddings"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    email_id = Column(String, index=True, nullable=False)
    embedding = Column(JSON)  # Vector embedding as JSON array
    created_at = Column(DateTime, server_default=func.now())
