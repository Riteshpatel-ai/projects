"""
Seed Sample Email Data for Testing
Run this to populate the database with sample hospital emails
"""
from datetime import datetime, timedelta
import random
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import EmailRecord
import uuid

# Sample data templates
CATEGORIES = [
    "Diagnostic Report",
    "Insurance Claim",
    "Patient Message",
    "Billing",
    "Appointment Confirmation",
    "Medical Report",
    "Doctor / Patient Communication"
]

PRIORITIES = ["high", "medium", "low"]
STATUSES = ["unread", "pending", "processed", "archived"]

SAMPLE_EMAILS = [
    {
        "sender": "lab@hospital.com",
        "subject": "Blood Test Results - Patient #{patient_id}",
        "category": "Diagnostic Report",
        "priority": "high",
        "summary": "Complete blood count results show normal values. All markers within acceptable range.",
        "entities": {"patient_name": "John Doe", "doctor": "Dr. Sarah Chen", "department": "Cardiology"}
    },
    {
        "sender": "insurance@careplus.com",
        "subject": "Claim #78{claim_num} - Approval Needed",
        "category": "Insurance Claim",
        "priority": "medium",
        "summary": "Insurance claim pending approval. Additional documentation may be required.",
        "entities": {"claim_amount": "$4,500", "patient_name": "Jane Smith", "provider": "CarePlus Insurance"}
    },
    {
        "sender": "patient@email.com",
        "subject": "Appointment Rescheduling Request",
        "category": "Patient Message",
        "priority": "low",
        "summary": "Patient requesting to reschedule appointment due to personal commitment.",
        "entities": {"patient_name": "Robert Johnson", "requested_date": "2025-11-05", "department": "ENT"}
    },
    {
        "sender": "billing@hospital.com",
        "subject": "Payment Confirmation - Invoice #{invoice_num}",
        "category": "Billing",
        "priority": "low",
        "summary": "Payment successfully processed. Receipt attached for your records.",
        "entities": {"amount": "$2,300", "patient_name": "Maria Garcia", "payment_method": "Insurance + Cash"}
    },
    {
        "sender": "radiology@hospital.com",
        "subject": "X-Ray Results - Patient #{patient_id}",
        "category": "Diagnostic Report",
        "priority": "high",
        "summary": "Chest X-ray shows clear lung fields. No abnormalities detected.",
        "entities": {"patient_name": "David Lee", "doctor": "Dr. James Wilson", "department": "Radiology"}
    },
    {
        "sender": "cardiology@hospital.com",
        "subject": "ECG Report - Urgent Review Required",
        "category": "Medical Report",
        "priority": "high",
        "summary": "ECG shows irregular heart rhythm. Immediate follow-up recommended.",
        "entities": {"patient_name": "Emily Brown", "doctor": "Dr. Sarah Chen", "department": "Cardiology"}
    },
    {
        "sender": "pharmacy@hospital.com",
        "subject": "Prescription Refill Reminder",
        "category": "Doctor / Patient Communication",
        "priority": "medium",
        "summary": "Patient prescription due for refill. Please review and authorize.",
        "entities": {"patient_name": "Michael Davis", "medication": "Metformin", "department": "Endocrinology"}
    },
    {
        "sender": "appointments@hospital.com",
        "subject": "Appointment Confirmation - {appointment_date}",
        "category": "Appointment Confirmation",
        "priority": "low",
        "summary": "Appointment confirmed for routine checkup. Please arrive 15 minutes early.",
        "entities": {"patient_name": "Sarah Wilson", "doctor": "Dr. Maria Garcia", "appointment_time": "10:00 AM"}
    },
    {
        "sender": "insurance@bluecross.com",
        "subject": "Claim Approved - Payment Processing",
        "category": "Insurance Claim",
        "priority": "medium",
        "summary": "Insurance claim approved. Payment will be processed within 5-7 business days.",
        "entities": {"claim_amount": "$12,300", "patient_name": "Thomas Anderson", "claim_id": "BC78945"}
    },
    {
        "sender": "emergency@hospital.com",
        "subject": "Emergency Report - Immediate Attention",
        "category": "Medical Report",
        "priority": "high",
        "summary": "Patient admitted to ER with acute symptoms. Urgent medical intervention required.",
        "entities": {"patient_name": "Lisa Johnson", "doctor": "Dr. Emergency Team", "department": "Emergency"}
    }
]

def seed_emails(db: Session, count: int = 50):
    """
    Seed database with sample emails
    
    Args:
        db: Database session
        count: Number of emails to create
    """
    print(f"🌱 Seeding {count} sample emails...")
    
    # Check if emails already exist
    existing_count = db.query(EmailRecord).count()
    if existing_count > 0:
        print(f"⚠️  Database already has {existing_count} emails.")
        response = input("Do you want to add more? (y/n): ")
        if response.lower() != 'y':
            print("Skipping seed.")
            return
    
    created = 0
    for i in range(count):
        # Select random template
        template = random.choice(SAMPLE_EMAILS)
        
        # Generate dynamic values
        patient_id = random.randint(1000, 9999)
        claim_num = random.randint(100, 999)
        invoice_num = random.randint(1000, 9999)
        
        # Generate timestamp (last 30 days)
        days_ago = random.randint(0, 30)
        timestamp = datetime.now() - timedelta(days=days_ago, hours=random.randint(0, 23))
        
        # Format subject with dynamic values
        subject = template["subject"].format(
            patient_id=patient_id,
            claim_num=claim_num,
            invoice_num=invoice_num,
            appointment_date=(datetime.now() + timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
        )
        
        # Create email record
        email = EmailRecord(
            gmail_id=f"gmail_{uuid.uuid4().hex[:16]}",
            thread_id=f"thread_{uuid.uuid4().hex[:16]}",
            sender=template["sender"],
            recipient="admin@hospital.com",
            subject=subject,
            timestamp=timestamp,
            category=template["category"],
            priority=template["priority"],
            summary=template["summary"],
            content=f"{subject}\n\n{template['summary']}\n\nFull email content would go here...",
            entities=template["entities"],
            status=random.choice(STATUSES),
            confidence_score=random.uniform(0.85, 0.99),
            attachments=[],
        )
        
        db.add(email)
        created += 1
        
        if (created) % 10 == 0:
            print(f"  Created {created}/{count} emails...")
    
    db.commit()
    print(f"✅ Successfully created {created} sample emails!")
    
    # Print statistics
    print("\n📊 Statistics:")
    for category in CATEGORIES:
        cat_count = db.query(EmailRecord).filter(EmailRecord.category == category).count()
        print(f"  {category}: {cat_count}")
    
    for priority in PRIORITIES:
        pri_count = db.query(EmailRecord).filter(EmailRecord.priority == priority).count()
        print(f"  Priority {priority}: {pri_count}")


def main():
    """Main execution"""
    print("=" * 60)
    print("MedMail Intelligence - Sample Data Seeder")
    print("=" * 60)
    
    db = SessionLocal()
    try:
        seed_emails(db, count=50)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.rollback()
    finally:
        db.close()
    
    print("\n🎉 Seeding complete!")


if __name__ == "__main__":
    main()
