"""
Email Management Routes
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from google.oauth2.credentials import Credentials

from app.db.database import get_db
from app.db.models import EmailRecord, User
from app.services.gmail_service import GmailService
from app.services.ai_categorizer import EmailCategorizer
from app.services.rag_service import rag_service
from app.routes.auth_routes import get_current_user
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


class EmailResponse(BaseModel):
    id: str
    sender: str
    subject: str
    timestamp: datetime
    category: Optional[str]
    priority: Optional[str]
    summary: Optional[str]
    status: str
    entities: Optional[dict]
    attachments: Optional[list]
    
    class Config:
        from_attributes = True


@router.post("/sync")
async def sync_emails(
    background_tasks: BackgroundTasks,
    days: int = 7,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Sync emails from Gmail"""
    if not current_user.gmail_access_token:
        raise HTTPException(
            status_code=400,
            detail="Gmail not connected. Please authorize first."
        )
    
    # Add sync task to background
    background_tasks.add_task(
        sync_emails_task,
        current_user,
        db,
        days
    )
    
    return {"message": "Email sync started", "status": "processing"}


async def sync_emails_task(user: User, db: Session, days: int):
    """Background task to sync and process emails"""
    try:
        # Create Gmail service with user credentials
        # Include client_id, client_secret and token_uri so credentials can refresh tokens
        try:
            credentials = Credentials(
                token=user.gmail_access_token,
                refresh_token=user.gmail_refresh_token,
                token_uri="https://oauth2.googleapis.com/token",
                client_id=settings.GMAIL_CLIENT_ID,
                client_secret=settings.GMAIL_CLIENT_SECRET,
            )

            gmail_service = GmailService(credentials)
        except Exception as e:
            logger.exception("Failed to create Gmail credentials for user %s", user.email)
            return
        
        # Fetch emails
        emails = await gmail_service.fetch_recent_emails(
            max_results=100,
            days=days
        )
        
        # Process each email
        for email_data in emails:
            # Check if email already exists
            existing = db.query(EmailRecord).filter(
                EmailRecord.gmail_id == email_data['gmail_id']
            ).first()
            
            if existing:
                continue
            
            # Categorize email using AI
            ai_result = await EmailCategorizer.categorize_email(email_data)
            
            # Create email record
            email_record = EmailRecord(
                gmail_id=email_data['gmail_id'],
                thread_id=email_data['thread_id'],
                sender=email_data['sender'],
                recipient=email_data['recipient'],
                subject=email_data['subject'],
                timestamp=email_data['timestamp'],
                content=email_data['content'],
                category=ai_result['category'],
                priority=ai_result['priority'],
                summary=ai_result['summary'],
                entities=ai_result['entities'],
                attachments=email_data['attachments'],
                confidence_score=ai_result.get('confidence', 0.0)
            )
            
            db.add(email_record)
        
        db.commit()
        
        # Rebuild RAG index
        await rag_service.build_index(db)
        
    except Exception as e:
        logger.exception("Error syncing emails for user %s: %s", user.email, str(e))


@router.get("/", response_model=List[EmailResponse])
async def get_emails(
    skip: int = 0,
    limit: int = 50,
    category: Optional[str] = None,
    priority: Optional[str] = None,
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get emails with filters"""
    query = db.query(EmailRecord).filter(EmailRecord.is_deleted == False)
    
    if category:
        query = query.filter(EmailRecord.category == category)
    if priority:
        query = query.filter(EmailRecord.priority == priority)
    if status:
        query = query.filter(EmailRecord.status == status)
    
    emails = query.order_by(EmailRecord.timestamp.desc()).offset(skip).limit(limit).all()
    return emails


@router.get("/{email_id}", response_model=EmailResponse)
async def get_email(
    email_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific email by ID"""
    email = db.query(EmailRecord).filter(
        EmailRecord.id == email_id,
        EmailRecord.is_deleted == False
    ).first()
    
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    
    return email


@router.patch("/{email_id}/status")
async def update_email_status(
    email_id: str,
    status: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update email status"""
    email = db.query(EmailRecord).filter(EmailRecord.id == email_id).first()
    
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    
    email.status = status
    if status == "processed":
        email.processed_at = datetime.utcnow()
    
    db.commit()
    
    return {"message": "Status updated", "status": status}


@router.delete("/{email_id}")
async def delete_email(
    email_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Soft delete email"""
    email = db.query(EmailRecord).filter(EmailRecord.id == email_id).first()
    
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    
    email.is_deleted = True
    db.commit()
    
    return {"message": "Email deleted"}
