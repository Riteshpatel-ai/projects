"""
Check and create admin user
"""
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_path))

from app.db.database import SessionLocal
from app.db.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def check_and_create_admin():
    db = SessionLocal()
    
    try:
        # Check existing users
        users = db.query(User).all()
        print(f"\n✅ Total users in database: {len(users)}")
        
        for user in users:
            print(f"   - {user.email} (ID: {user.id})")
        
        # Check for admin user
        admin_email = "admin@hospital.com"
        admin = db.query(User).filter(User.email == admin_email).first()
        
        if admin:
            print(f"\n✅ Admin user already exists: {admin_email}")
            
            # Test password verification
            test_password = "admin123"
            is_valid = pwd_context.verify(test_password, admin.hashed_password)
            print(f"   Password 'admin123' verification: {is_valid}")
            
            if not is_valid:
                print("\n⚠️  Password mismatch! Updating password...")
                admin.hashed_password = pwd_context.hash(test_password)
                db.commit()
                print("   ✅ Password updated successfully!")
        else:
            print(f"\n❌ Admin user not found. Creating: {admin_email}")
            
            # Create admin user
            hashed_password = pwd_context.hash("admin123")
            new_admin = User(
                email=admin_email,
                hashed_password=hashed_password,
                full_name="Admin User"
            )
            
            db.add(new_admin)
            db.commit()
            db.refresh(new_admin)
            
            print(f"   ✅ Admin user created successfully!")
            print(f"   Email: {admin_email}")
            print(f"   Password: admin123")
            print(f"   ID: {new_admin.id}")
        
        print("\n" + "="*50)
        print("You can now login with:")
        print("Email: admin@hospital.com")
        print("Password: admin123")
        print("="*50 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    check_and_create_admin()
