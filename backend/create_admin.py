"""
Simple script to create admin user
"""
from app.db.database import SessionLocal
from app.db.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db = SessionLocal()

try:
    # Check if admin exists
    admin = db.query(User).filter(User.email == "admin@hospital.com").first()
    
    if admin:
        print("✅ Admin already exists!")
        print(f"Email: {admin.email}")
    else:
        # Create admin
        hashed_password = pwd_context.hash("admin123")
        admin = User(
            email="admin@hospital.com",
            hashed_password=hashed_password,
            full_name="Admin User"
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        
        print("✅ Admin user created!")
        print(f"Email: admin@hospital.com")
        print(f"Password: admin123")
        print(f"ID: {admin.id}")
    
    # Show all users
    all_users = db.query(User).all()
    print(f"\n📊 Total users: {len(all_users)}")
    for u in all_users:
        print(f"   - {u.email}")
        
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    db.close()
