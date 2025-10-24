# Install backend dependencies
Write-Host "Installing backend dependencies..." -ForegroundColor Green
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Create .env file if not exists
if (-not (Test-Path .env)) {
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "⚠️  Please edit backend/.env with your API keys!" -ForegroundColor Yellow
}

# Initialize database
Write-Host "Initializing database..." -ForegroundColor Green
python -c "from app.db.database import Base, engine; Base.metadata.create_all(bind=engine)"

cd ..

# Install frontend dependencies
Write-Host "Installing frontend dependencies..." -ForegroundColor Green
npm install

# Create frontend .env if not exists
if (-not (Test-Path .env)) {
    Write-Host "Creating frontend .env file..." -ForegroundColor Yellow
    "VITE_API_URL=http://localhost:8000" | Out-File -FilePath .env -Encoding utf8
}

Write-Host ""
Write-Host "✅ Setup completed!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Edit backend/.env with your API keys" -ForegroundColor White
Write-Host "2. Start backend: cd backend && .\venv\Scripts\Activate.ps1 && uvicorn app.main:app --reload" -ForegroundColor White
Write-Host "3. Start frontend: npm run dev" -ForegroundColor White
Write-Host ""
Write-Host "See SETUP_GUIDE.md for detailed instructions" -ForegroundColor Cyan
