# Production / Docker Quickstart

This file explains how to run the project locally using Docker for a production-like environment.

Prerequisites:
- Docker & Docker Compose installed
- Copy `backend/.env.example` to `backend/.env` and fill values (do not commit secrets)

Start the stack:

```bash
docker compose up --build
```

This will start:
- Postgres on 5432
- Backend FastAPI on 8000
- Frontend (Vite) served via nginx on 5173

Notes:
- The compose setup is for local integration testing and not production-grade. For production, build images and deploy to a container platform, use managed DB, add TLS, secrets management, and monitoring.
