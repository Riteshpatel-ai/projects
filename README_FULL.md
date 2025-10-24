# 🏥 MedMail Intelligence Platform

> AI-driven hospital email classification & analytics system with RAG-powered natural language queries

[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.3-61DAFB.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.8-3178C6.svg)](https://www.typescriptlang.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-316192.svg)](https://www.postgresql.org/)

## 📋 Overview

MedMail Intelligence Platform transforms hospital email chaos into actionable insights using AI. It automatically categorizes, extracts data, and enables natural language queries across all hospital communications.

### ✨ Key Features

- **🤖 AI-Powered Classification**: Automatic email categorization using GPT-4
- **📧 Gmail Integration**: Seamless OAuth2 connection to fetch and process emails
- **🔍 RAG Queries**: Natural language search using vector similarity (FAISS)
- **📊 Real-time Analytics**: Interactive dashboards with trends and insights
- **🏷️ Entity Extraction**: Automatic extraction of patient names, doctors, departments, amounts
- **📈 Visual Analytics**: Charts, trends, and performance metrics
- **🔐 Secure Authentication**: JWT-based auth with bcrypt password hashing

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React + Vite)                   │
│  ┌──────────┬────────────┬──────────────┬──────────────┐   │
│  │   Hero   │  Dashboard │  Analytics   │ AI Assistant │   │
│  └──────────┴────────────┴──────────────┴──────────────┘   │
└──────────────────────┬──────────────────────────────────────┘
                       │ REST API (Axios)
┌──────────────────────▼──────────────────────────────────────┐
│                  Backend (FastAPI + Python)                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Routes: Auth │ Emails │ Analytics │ Query (RAG)      │ │
│  ├────────────────────────────────────────────────────────┤ │
│  │  Services: Gmail │ AI Categorizer │ RAG │ Extractor  │ │
│  ├────────────────────────────────────────────────────────┤ │
│  │  Database: PostgreSQL (SQLAlchemy ORM)                │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────┬───────────────────────┬──────────────────────┘
               │                       │
         ┌─────▼──────┐         ┌─────▼─────┐
         │  OpenAI    │         │   Gmail   │
         │  GPT-4     │         │   API     │
         └────────────┘         └───────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- **Node.js**: v20 or higher
- **Python**: 3.11 or higher
- **PostgreSQL**: 15 or higher
- **OpenAI API Key**
- **Gmail OAuth Credentials**

### Option 1: Using Docker (Recommended)

1. **Clone the repository**
```bash
git clone <repository-url>
cd projects
```

2. **Set up environment variables**
```bash
cp .env.docker .env
# Edit .env and add your API keys
```

3. **Start all services**
```bash
docker-compose up -d
```

4. **Access the application**
- Frontend: http://localhost:8080
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/docs

### Option 2: Manual Setup

#### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your credentials

# Run database migrations (first time)
python -c "from app.db.database import Base, engine; Base.metadata.create_all(bind=engine)"

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
# Navigate to project root
cd ..

# Install dependencies
npm install

# Start development server
npm run dev
```

---

## 📁 Project Structure

```
projects/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py          # Configuration management
│   │   │   └── __init__.py
│   │   ├── db/
│   │   │   ├── database.py        # Database connection
│   │   │   ├── models.py          # SQLAlchemy models
│   │   │   └── __init__.py
│   │   ├── routes/
│   │   │   ├── auth_routes.py     # Authentication endpoints
│   │   │   ├── email_routes.py    # Email management
│   │   │   ├── analytics_routes.py # Analytics endpoints
│   │   │   ├── query_routes.py    # RAG queries
│   │   │   └── __init__.py
│   │   ├── services/
│   │   │   ├── gmail_service.py   # Gmail API integration
│   │   │   ├── ai_categorizer.py  # GPT-4 categorization
│   │   │   ├── rag_service.py     # Vector search & RAG
│   │   │   └── __init__.py
│   │   ├── utils/                 # Utility functions
│   │   └── main.py                # FastAPI application
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── src/
│   ├── api/
│   │   ├── client.ts              # Axios configuration
│   │   ├── auth.ts                # Auth API calls
│   │   ├── emails.ts              # Email API calls
│   │   ├── analytics.ts           # Analytics API calls
│   │   ├── query.ts               # Query API calls
│   │   └── index.ts
│   ├── components/
│   │   ├── Hero.tsx               # Landing page
│   │   ├── Dashboard.tsx          # Email dashboard
│   │   ├── Analytics.tsx          # Analytics view
│   │   ├── AIAssistant.tsx        # RAG query interface
│   │   └── ui/                    # shadcn/ui components
│   ├── pages/
│   │   ├── Index.tsx              # Main page
│   │   └── NotFound.tsx
│   ├── App.tsx
│   └── main.tsx
├── docker-compose.yml
├── package.json
└── README.md
```

---

## 🔧 Configuration

### Backend Environment Variables

Create `.env` in the `backend/` directory:

```env
# OpenAI
OPENAI_API_KEY=sk-your-key-here
EMBEDDING_MODEL=text-embedding-ada-002

# Gmail OAuth2
GMAIL_CLIENT_ID=your-client-id.apps.googleusercontent.com
GMAIL_CLIENT_SECRET=your-client-secret
GMAIL_REDIRECT_URI=http://localhost:8000/api/auth/gmail/callback

# Database
DATABASE_URL=postgresql://medmail_user:medmail_password@localhost:5432/medmail_db

# JWT Security
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Application
APP_NAME=MedMail Intelligence Platform
DEBUG=True
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:8080
```

### Frontend Environment Variables

Create `.env` in the project root:

```env
VITE_API_URL=http://localhost:8000
```

---

## 📚 API Documentation

Once the backend is running, visit:

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

### Main Endpoints

#### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user
- `GET /api/auth/gmail/authorize` - Get Gmail auth URL
- `GET /api/auth/gmail/callback` - Handle OAuth callback

#### Emails
- `POST /api/emails/sync` - Sync emails from Gmail
- `GET /api/emails/` - List emails with filters
- `GET /api/emails/{id}` - Get specific email
- `PATCH /api/emails/{id}/status` - Update email status
- `DELETE /api/emails/{id}` - Delete email

#### Analytics
- `GET /api/analytics/overview` - Get analytics overview
- `GET /api/analytics/categories` - Category distribution
- `GET /api/analytics/trends` - Email volume trends
- `GET /api/analytics/top-senders` - Top email senders
- `GET /api/analytics/departments` - Department statistics

#### RAG Queries
- `POST /api/query/` - Natural language email query
- `POST /api/query/rebuild-index` - Rebuild vector index
- `GET /api/query/history` - Query history

---

## 🎯 Usage Examples

### Natural Language Queries

```javascript
// Frontend example
import { queryApi } from '@/api';

const results = await queryApi.query("Show urgent diagnostic results from last week");
const results = await queryApi.query("All insurance claims above $5000");
const results = await queryApi.query("Patient messages from cardiology department");
```

### Email Categorization

The AI automatically categorizes emails into:
- Doctor / Patient Communication
- Diagnostic Results
- Insurance Claims
- Billing / Payment
- Appointment Confirmation
- Official Notice
- Medical Report
- Prescription
- Lab Results

### Entity Extraction

Automatically extracts:
- Patient names
- Doctor names
- Departments
- Monetary amounts
- Important dates
- Diagnosis information
- Claim/Invoice IDs
- Appointment dates

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
npm run test
```

---

## 🚢 Deployment

### Using Docker

```bash
# Build and deploy all services
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Manual Deployment

#### Backend (Render, AWS, etc.)
1. Set environment variables
2. Run database migrations
3. Deploy FastAPI app with uvicorn

#### Frontend (Vercel, Netlify, etc.)
1. Set `VITE_API_URL` to your backend URL
2. Run `npm run build`
3. Deploy the `dist` folder

---

## 🔐 Security Best Practices

- ✅ JWT-based authentication
- ✅ Password hashing with bcrypt
- ✅ OAuth2 for Gmail integration
- ✅ Environment variable management
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ CORS configuration
- ✅ Input validation (Pydantic)

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Relational database
- **SQLAlchemy** - ORM
- **OpenAI GPT-4** - AI categorization
- **LangChain** - RAG framework
- **FAISS** - Vector similarity search
- **Gmail API** - Email fetching

### Frontend
- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **shadcn/ui** - Component library
- **Axios** - HTTP client
- **React Query** - Data fetching
- **Recharts** - Data visualization

---

## 📝 License

This project is licensed under the MIT License.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📧 Support

For support, email support@medmail-intelligence.com or open an issue on GitHub.

---

Made with ❤️ by the MedMail Team
