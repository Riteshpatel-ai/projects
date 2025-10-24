"""
Initialize PostgreSQL Database
Run this to create all tables in PostgreSQL
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.database import engine, Base
from app.db.models import EmailRecord, User, QueryHistory, EmailEmbedding
from sqlalchemy import inspect
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db():
    """Initialize database tables"""
    try:
        logger.info("🔧 Connecting to PostgreSQL database...")
        
        # Test connection
        inspector = inspect(engine)
        logger.info("✅ Database connection successful!")
        
        # Check existing tables
        existing_tables = inspector.get_table_names()
        logger.info(f"📋 Existing tables: {existing_tables}")
        
        # Create all tables
        logger.info("🏗️  Creating database tables...")
        Base.metadata.create_all(bind=engine)
        
        # Verify tables created
        inspector = inspect(engine)
        new_tables = inspector.get_table_names()
        logger.info(f"✅ Tables in database: {new_tables}")
        
        logger.info("\n🎉 Database initialization complete!")
        logger.info("\nTables created:")
        for table in new_tables:
            logger.info(f"  ✓ {table}")
        
        logger.info("\n📝 Next steps:")
        logger.info("  1. Run seed script: python -m app.utils.seed_data")
        logger.info("  2. Start backend: python -m uvicorn app.main:app --reload")
        logger.info("  3. Access API docs: http://localhost:8000/api/docs")
        
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        logger.error("\n💡 Troubleshooting:")
        logger.error("  1. Check PostgreSQL is running")
        logger.error("  2. Verify credentials in backend/.env")
        logger.error("  3. Ensure database 'postgres' exists")
        logger.error("  4. Check connection string format")
        sys.exit(1)


if __name__ == "__main__":
    init_db()
