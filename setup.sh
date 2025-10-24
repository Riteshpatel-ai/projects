#!/bin/bash

echo "🚀 Setting up MedMail Intelligence Platform..."

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env file if not exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit backend/.env with your API keys!"
fi

# Initialize database
echo "🗄️  Initializing database..."
python -c "from app.db.database import Base, engine; Base.metadata.create_all(bind=engine)"

cd ..

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
npm install

# Create frontend .env if not exists
if [ ! -f .env ]; then
    echo "📝 Creating frontend .env file..."
    echo "VITE_API_URL=http://localhost:8000" > .env
fi

echo ""
echo "✅ Setup completed!"
echo ""
echo "Next steps:"
echo "1. Edit backend/.env with your API keys"
echo "2. Start backend: cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo "3. Start frontend: npm run dev"
echo ""
echo "See SETUP_GUIDE.md for detailed instructions"
