# MedMail Intelligence Platform - Quick Start Guide

## 🚀 Quick Start (Development)

### 1. Start Backend (Terminal 1)
```powershell
cd c:\Users\Rites\OneDrive\Desktop\projects
.\.venv\Scripts\Activate.ps1
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Seed Sample Data (Terminal 2 - First Time Only)
```powershell
cd c:\Users\Rites\OneDrive\Desktop\projects
.\.venv\Scripts\Activate.ps1
cd backend
python -m app.utils.seed_data
```

### 3. Start Frontend (Terminal 3)
```powershell
cd c:\Users\Rites\OneDrive\Desktop\projects
npm run dev
```

### 4. Access Application
- Frontend: http://localhost:5173
- Backend API Docs: http://localhost:8000/api/docs
- Health Check: http://localhost:8000/health

---

## 📝 First Time Setup

### Create Admin User
```bash
# Register via Frontend UI or API
POST http://localhost:8000/api/auth/register
{
  "email": "admin@hospital.com",
  "password": "admin123",
  "full_name": "Admin User"
}
```

### Sync Gmail (Optional - Requires OAuth Setup)
```bash
# Via Frontend Dashboard or API
POST http://localhost:8000/api/emails/sync?days=30
```

---

## 🔧 Production Deployment

### Using Docker
```powershell
docker-compose up --build -d
```

### Manual Deployment

#### Backend
```powershell
# Set environment variables
$env:DATABASE_URL="your_postgres_url"
$env:OPENAI_API_KEY="your_key"

# Run with gunicorn
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

#### Frontend
```powershell
npm run build
# Serve the dist folder with nginx or similar
```

---

## 🔍 Troubleshooting

### Backend won't start
- Check `.env` file in `backend/` folder
- Verify Python dependencies: `pip list`
- Check database connection
- View logs for errors

### Frontend can't connect to backend
- Check `VITE_API_URL` in `.env`
- Ensure backend is running on port 8000
- Check browser console for CORS errors

### RAG queries returning same results
- Rebuild index: `POST /api/query/rebuild-index`
- Check OpenAI API key is valid
- Verify emails exist in database

### No emails in dashboard
- Run seed script: `python -m app.utils.seed_data`
- Or sync from Gmail
- Check database has email records

---

## 🎯 Key Features to Test

1. **Dashboard** - View and filter emails
2. **Analytics** - Charts and statistics
3. **AI Assistant** - Natural language queries
   - Try: "Show urgent emails from today"
   - Try: "Pending insurance claims"
   - Try: "Emails from cardiology department"

---

## 🐛 Known Issues & Fixes

### Issue: RAG returning same results
**Fix Applied**: Added embedding cache and index persistence

### Issue: No mock data
**Fix Applied**: Created seed_data.py script

### Issue: Frontend not connected
**Fix Applied**: Integrated React Query with API

---

## 📚 API Endpoints

### Authentication
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user

### Emails
- `GET /api/emails/` - List emails (with filters)
- `GET /api/emails/{id}` - Get specific email
- `POST /api/emails/sync` - Sync from Gmail
- `PATCH /api/emails/{id}/status` - Update status

### Analytics
- `GET /api/analytics/overview` - Dashboard stats
- `GET /api/analytics/trends` - Email trends
- `GET /api/analytics/by-category` - Category distribution

### AI Query
- `POST /api/query/` - Natural language query
- `POST /api/query/rebuild-index` - Rebuild RAG index
- `GET /api/query/history` - Query history

---

## 💡 Pro Tips

1. **Seed data first** before testing AI features
2. **Rebuild RAG index** after adding new emails
3. **Use specific queries** for better AI results
4. **Check API docs** at `/api/docs` for all endpoints
5. **Monitor logs** for debugging issues

---

## 📞 Support

For issues or questions:
1. Check logs in terminal
2. Review API docs at `/api/docs`
3. Check browser console for frontend errors
4. Verify all environment variables are set

---

**Happy Coding! 🎉**
