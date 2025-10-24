"""
RAG Query Routes - Natural Language Email Search
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from datetime import datetime

from app.db.database import get_db
from app.db.models import EmailRecord, User, QueryHistory
from app.services.rag_service import rag_service
from app.routes.auth_routes import get_current_user
import time

router = APIRouter()


class QueryRequest(BaseModel):
    query: str


class EmailResult(BaseModel):
    id: str
    sender: str
    subject: str
    timestamp: datetime
    category: str
    priority: str
    summary: str
    
    class Config:
        from_attributes = True


class QueryResponse(BaseModel):
    query: str
    results_count: int
    execution_time: float
    results: List[EmailResult]


@router.post("/", response_model=QueryResponse)
async def query_emails(
    request: QueryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Query emails using natural language
    
    Example queries:
    - "Show all insurance claims from last week"
    - "Urgent diagnostic results today"
    - "Billing emails above $5000"
    - "Patient messages from cardiology department"
    """
    start_time = time.time()
    
    try:
        # Perform RAG query
        results = await rag_service.query_emails(request.query, db)
        
        execution_time = time.time() - start_time
        
        # Save query history
        query_history = QueryHistory(
            user_id=current_user.id,
            query_text=request.query,
            results_count=len(results),
            execution_time=execution_time
        )
        db.add(query_history)
        db.commit()
        
        # Format results
        email_results = [
            EmailResult(
                id=email.id,
                sender=email.sender,
                subject=email.subject,
                timestamp=email.timestamp,
                category=email.category or 'Uncategorized',
                priority=email.priority or 'medium',
                summary=email.summary or ''
            )
            for email in results
        ]
        
        return QueryResponse(
            query=request.query,
            results_count=len(results),
            execution_time=round(execution_time, 3),
            results=email_results
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")


@router.post("/rebuild-index")
async def rebuild_index(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Rebuild the RAG vector index"""
    try:
        await rag_service.build_index(db)
        return {"message": "Index rebuilt successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history")
async def get_query_history(
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's query history"""
    history = db.query(QueryHistory).filter(
        QueryHistory.user_id == current_user.id
    ).order_by(QueryHistory.created_at.desc()).limit(limit).all()
    
    return [
        {
            "query": h.query_text,
            "results_count": h.results_count,
            "execution_time": h.execution_time,
            "timestamp": h.created_at
        }
        for h in history
    ]
