# 🚀 Quick Setup Guide

## Prerequisites Check

Before you begin, ensure you have:
- [ ] Node.js v20+ installed
- [ ] Python 3.11+ installed
- [ ] PostgreSQL 15+ installed (or use Docker)
- [ ] OpenAI API key
- [ ] Gmail OAuth credentials

---

## Step-by-Step Setup

### 1️⃣ Get API Keys

#### OpenAI API Key
1. Visit https://platform.openai.com/api-keys
2. Create a new API key
3. Copy and save it securely

#### Gmail OAuth Credentials
1. Go to https://console.cloud.google.com/
2. Create a new project or select existing
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Web application)
5. Add authorized redirect URI: `http://localhost:8000/api/auth/gmail/callback`
6. Copy Client ID and Client Secret

### 2️⃣ Clone and Install

```bash
# Clone repository
git clone <your-repo-url>
cd projects

# Install frontend dependencies
npm install

# Install backend dependencies
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cd ..
```

### 3️⃣ Configure Environment

#### Backend Configuration
```bash
cd backend
cp .env.example .env
```

Edit `backend/.env`:
```env
OPENAI_API_KEY=sk-your-actual-key-here
GMAIL_CLIENT_ID=your-client-id.apps.googleusercontent.com
GMAIL_CLIENT_SECRET=your-client-secret
DATABASE_URL=postgresql://medmail_user:medmail_password@localhost:5432/medmail_db
SECRET_KEY=generate-a-random-secret-key-here
```

#### Frontend Configuration
```bash
# Create .env in project root
echo "VITE_API_URL=http://localhost:8000" > .env
```

### 4️⃣ Setup Database

#### Option A: Using Docker (Easiest)
```bash
docker run --name medmail_postgres \
  -e POSTGRES_USER=medmail_user \
  -e POSTGRES_PASSWORD=medmail_password \
  -e POSTGRES_DB=medmail_db \
  -p 5432:5432 \
  -d postgres:15-alpine
```

#### Option B: Manual PostgreSQL Setup
```sql
CREATE DATABASE medmail_db;
CREATE USER medmail_user WITH PASSWORD 'medmail_password';
GRANT ALL PRIVILEGES ON DATABASE medmail_db TO medmail_user;
```

#### Initialize Database Tables
```bash
cd backend
python -c "from app.db.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

### 5️⃣ Start Development Servers

#### Terminal 1 - Backend
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Terminal 2 - Frontend
```bash
npm run dev
```

### 6️⃣ Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs

---

## 🎯 First Time Usage

### 1. Register an Account
- Open http://localhost:5173
- Click "Register" and create an account

### 2. Connect Gmail
- Login to your account
- Go to Settings/Profile
- Click "Connect Gmail"
- Authorize access

### 3. Sync Emails
- Click "Sync Inbox" button
- Wait for emails to be processed (this may take a few minutes)

### 4. Explore Features
- **Dashboard**: View categorized emails
- **Analytics**: See trends and statistics
- **AI Assistant**: Try natural language queries like:
  - "Show urgent emails from today"
  - "All diagnostic results from last week"
  - "Insurance claims pending approval"

---

## 🐳 Docker Quick Start (Alternative)

If you prefer Docker:

```bash
# Create .env file
cp .env.docker .env
# Edit .env with your API keys

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Access application
# Frontend: http://localhost:8080
# Backend: http://localhost:8000
```

---

## 🔧 Troubleshooting

### Issue: Database Connection Error
**Solution**: Check if PostgreSQL is running
```bash
# Check PostgreSQL status
docker ps  # If using Docker
# or
pg_isready  # If installed locally
```

### Issue: OpenAI API Error
**Solution**: Verify API key is correct and has credits
```bash
# Test API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Issue: Gmail OAuth Not Working
**Solution**: 
1. Check redirect URI matches exactly
2. Ensure Gmail API is enabled in Google Cloud Console
3. Check credentials are for "Web application" type

### Issue: CORS Error
**Solution**: Check ALLOWED_ORIGINS in backend/.env
```env
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:8080
```

---

## 📝 Next Steps

1. **Customize Categories**: Edit `ai_categorizer.py` to add custom categories
2. **Add More Entities**: Modify entity extraction in `ai_categorizer.py`
3. **Customize UI**: Update components in `src/components/`
4. **Add Authentication**: Implement proper user management
5. **Deploy**: Follow deployment guide in README_FULL.md

---

## 🆘 Need Help?

- **Documentation**: See README_FULL.md
- **API Reference**: http://localhost:8000/api/docs
- **Issues**: Open an issue on GitHub
- **Email**: support@medmail-intelligence.com

---

**Happy Coding! 🎉**
