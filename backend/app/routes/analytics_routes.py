"""
Analytics Routes
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from app.db.database import get_db
from app.db.models import EmailRecord, User
from app.routes.auth_routes import get_current_user

router = APIRouter()


class CategoryStats(BaseModel):
    category: str
    count: int
    percentage: float


class TrendData(BaseModel):
    date: str
    count: int


class SenderStats(BaseModel):
    sender: str
    count: int
    avg_response_time: Optional[float]


class AnalyticsOverview(BaseModel):
    total_emails: int
    unprocessed_count: int
    processed_today: int
    high_priority_count: int
    avg_response_time: float
    categories: List[CategoryStats]


@router.get("/overview", response_model=AnalyticsOverview)
async def get_analytics_overview(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive analytics overview"""
    
    # Total emails
    total_emails = db.query(func.count(EmailRecord.id)).filter(
        EmailRecord.is_deleted == False
    ).scalar()
    
    # Unprocessed
    unprocessed = db.query(func.count(EmailRecord.id)).filter(
        EmailRecord.is_deleted == False,
        EmailRecord.status != 'processed'
    ).scalar()
    
    # Processed today
    today = datetime.now().replace(hour=0, minute=0, second=0)
    processed_today = db.query(func.count(EmailRecord.id)).filter(
        EmailRecord.processed_at >= today
    ).scalar()
    
    # High priority
    high_priority = db.query(func.count(EmailRecord.id)).filter(
        EmailRecord.is_deleted == False,
        EmailRecord.priority == 'high'
    ).scalar()
    
    # Average response time (mock for now)
    avg_response_time = 2.8
    
    # Category distribution
    category_stats = db.query(
        EmailRecord.category,
        func.count(EmailRecord.id).label('count')
    ).filter(
        EmailRecord.is_deleted == False
    ).group_by(EmailRecord.category).all()
    
    categories = []
    for cat, count in category_stats:
        categories.append(CategoryStats(
            category=cat or 'Uncategorized',
            count=count,
            percentage=round((count / total_emails * 100) if total_emails > 0 else 0, 2)
        ))
    
    return AnalyticsOverview(
        total_emails=total_emails or 0,
        unprocessed_count=unprocessed or 0,
        processed_today=processed_today or 0,
        high_priority_count=high_priority or 0,
        avg_response_time=avg_response_time,
        categories=categories
    )


@router.get("/categories")
async def get_category_distribution(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get email distribution by category"""
    start_date = datetime.now() - timedelta(days=days)
    
    results = db.query(
        EmailRecord.category,
        func.count(EmailRecord.id).label('count')
    ).filter(
        EmailRecord.is_deleted == False,
        EmailRecord.timestamp >= start_date
    ).group_by(EmailRecord.category).all()
    
    total = sum(count for _, count in results)
    
    return [
        {
            "category": cat or 'Uncategorized',
            "count": count,
            "percentage": round((count / total * 100) if total > 0 else 0, 2)
        }
        for cat, count in results
    ]


@router.get("/trends", response_model=List[TrendData])
async def get_email_trends(
    days: int = 7,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get email volume trends"""
    start_date = datetime.now() - timedelta(days=days)
    
    results = db.query(
        func.date(EmailRecord.timestamp).label('date'),
        func.count(EmailRecord.id).label('count')
    ).filter(
        EmailRecord.is_deleted == False,
        EmailRecord.timestamp >= start_date
    ).group_by(func.date(EmailRecord.timestamp)).order_by('date').all()
    
    return [
        TrendData(
            date=date.strftime('%Y-%m-%d'),
            count=count
        )
        for date, count in results
    ]


@router.get("/top-senders")
async def get_top_senders(
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get top email senders"""
    results = db.query(
        EmailRecord.sender,
        func.count(EmailRecord.id).label('count')
    ).filter(
        EmailRecord.is_deleted == False
    ).group_by(EmailRecord.sender).order_by(desc('count')).limit(limit).all()
    
    return [
        {
            "sender": sender,
            "count": count
        }
        for sender, count in results
    ]


@router.get("/attachments")
async def get_attachment_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get attachment statistics"""
    emails_with_attachments = db.query(EmailRecord).filter(
        EmailRecord.is_deleted == False,
        EmailRecord.attachments != None
    ).all()
    
    attachment_types = {}
    total_size = 0
    
    for email in emails_with_attachments:
        if email.attachments:
            for att in email.attachments:
                mime_type = att.get('mime_type', 'unknown')
                attachment_types[mime_type] = attachment_types.get(mime_type, 0) + 1
                total_size += att.get('size', 0)
    
    return {
        "total_attachments": sum(attachment_types.values()),
        "total_size_mb": round(total_size / (1024 * 1024), 2),
        "types": [
            {"type": type_name, "count": count}
            for type_name, count in attachment_types.items()
        ]
    }


@router.get("/departments")
async def get_department_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get department-wise email statistics"""
    emails = db.query(EmailRecord).filter(
        EmailRecord.is_deleted == False,
        EmailRecord.entities != None
    ).all()
    
    departments = {}
    
    for email in emails:
        if email.entities and 'department' in email.entities:
            dept = email.entities['department']
            if dept:
                if dept not in departments:
                    departments[dept] = {'count': 0, 'emails': []}
                departments[dept]['count'] += 1
                departments[dept]['emails'].append(email.id)
    
    return [
        {
            "department": dept,
            "email_count": data['count'],
            "avg_response_time": f"{round(2 + (i * 0.5), 1)}h"  # Mock data
        }
        for i, (dept, data) in enumerate(departments.items())
    ]
