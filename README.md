# 🏥 MedMail Intelligence Platform

> Transform hospital email chaos into actionable insights with AI-powered automation

[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.3-61DAFB.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.8-3178C6.svg)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 🌟 Features

- **🤖 AI Email Categorization** - GPT-4 powered automatic classification
- **📧 Gmail Integration** - Seamless OAuth2 connection
- **🔍 RAG Queries** - Natural language email search using FAISS
- **📊 Real-time Analytics** - Interactive dashboards and trends
- **🏷️ Entity Extraction** - Automatic data extraction from emails
- **🔐 Secure Auth** - JWT-based authentication with OAuth2

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# 1. Copy environment file and add your API keys
cp .env.docker .env

# 2. Start all services
docker-compose up -d

# 3. Access the app
# Frontend: http://localhost:8080
# Backend API: http://localhost:8000/api/docs
```

### Manual Setup

```bash
# Windows
.\setup.ps1

# Linux/Mac
chmod +x setup.sh && ./setup.sh

# Start backend (Terminal 1)
cd backend && .\venv\Scripts\Activate && uvicorn app.main:app --reload

# Start frontend (Terminal 2)
npm run dev
```

## 📚 Documentation

- **[Complete Setup Guide](SETUP_GUIDE.md)** - Step-by-step instructions
- **[Full Documentation](README_FULL.md)** - Architecture and API reference
- **[Project Summary](PROJECT_COMPLETE.md)** - What's been built
- **[API Documentation](http://localhost:8000/api/docs)** - Interactive Swagger UI

## 🏗️ Project Structure

```
projects/
├── backend/          # FastAPI backend with AI services
│   ├── app/
│   │   ├── routes/   # API endpoints
│   │   ├── services/ # Gmail, AI, RAG services
│   │   ├── db/       # Database models
│   │   └── core/     # Configuration
│   └── requirements.txt
├── src/              # React frontend
│   ├── api/          # API client layer
│   ├── components/   # UI components
│   └── pages/        # Route pages
└── docker-compose.yml
```

## 🛠️ Tech Stack

**Backend**
- FastAPI, PostgreSQL, SQLAlchemy
- OpenAI GPT-4, LangChain, FAISS
- Gmail API, JWT Auth

**Frontend**
- React 18, TypeScript, Vite
- Tailwind CSS, shadcn/ui
- Axios, React Query, Recharts

## 🎯 Key Endpoints

```
POST /api/auth/login              # User authentication
POST /api/emails/sync             # Sync from Gmail
GET  /api/emails/                 # List emails
POST /api/query/                  # Natural language query
GET  /api/analytics/overview      # Analytics dashboard
```

## 📖 Example Usage

### Natural Language Queries
```javascript
// "Show urgent diagnostic results from last week"
// "All insurance claims above $5000"
// "Patient messages from cardiology"
```

### Email Categories
- Doctor/Patient Communication
- Diagnostic Results
- Insurance Claims
- Billing/Payment
- Appointment Confirmation
- Medical Reports & more

## 🔐 Environment Variables

Required in `backend/.env`:
```env
OPENAI_API_KEY=your-key
GMAIL_CLIENT_ID=your-client-id
GMAIL_CLIENT_SECRET=your-secret
DATABASE_URL=postgresql://...
SECRET_KEY=your-jwt-secret
```

## 🤝 Contributing

Contributions welcome! Please read our contributing guidelines first.

## 📝 License

MIT License - see LICENSE file for details

## 🆘 Support

- **Issues**: Open a GitHub issue
- **Email**: support@medmail-intelligence.com
- **Docs**: See documentation files

---

**Built with ❤️ for healthcare professionals**
"# projects" 
