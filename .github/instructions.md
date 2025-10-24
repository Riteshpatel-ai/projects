Excellent — now we’re moving into **implementation phase** 👨‍💻

Since your project involves **backend (AI + Gmail + DB)** and **frontend (dashboard + RAG)**, we can guide **GitHub Copilot** (or Copilot Workspace / IntelliJ AI) to generate high-quality code automatically.

Below is a **complete “Copilot instruction file”** (you can paste it into a `README.md`, or use it as a **system prompt for Copilot Chat**) so it knows *exactly* what to build and how.

---

# 🧠 GitHub Copilot Project Instruction

**Project:** MedMail Intelligence Dashboard
**Goal:** Build an AI-driven hospital email classification & analytics system.

---

## 🔧 Project Overview

> Copilot, you are helping to build a **full-stack AI app** that connects to Gmail, classifies hospital emails by category (Doctor/Patient Communication, Diagnostic Results, Insurance Claims, Billing, etc.), extracts key data from attachments, stores it in a database, and visualizes it in a React dashboard.

---

## 🏗️ Architecture Summary

| Layer              | Tech Stack                          |
| ------------------ | ----------------------------------- |
| **Frontend**       | React + Tailwind + Recharts + Axios |
| **Backend**        | FastAPI (Python)                    |
| **Database**       | PostgreSQL (SQLAlchemy ORM)         |
| **AI Models**      | OpenAI GPT-4 / LangChain            |
| **Vector Store**   | FAISS (for semantic queries)        |
| **Email Fetching** | Gmail API + OAuth2                  |
| **Deployment**     | Docker + Render / AWS               |

---

## 🧩 Backend Requirements (FastAPI)

### 1. Project Structure

```
backend/
 ├── app/
 │   ├── main.py
 │   ├── routes/
 │   │   ├── email_routes.py
 │   │   └── query_routes.py
 │   ├── services/
 │   │   ├── gmail_service.py
 │   │   ├── ai_categorizer.py
 │   │   └── entity_extractor.py
 │   ├── db/
 │   │   ├── models.py
 │   │   ├── database.py
 │   └── utils/
 │       ├── pdf_parser.py
 │       └── summarizer.py
 ├── requirements.txt
 └── Dockerfile
```

### 2. Gmail Integration

* Use Gmail API with OAuth2 to fetch recent emails + attachments.
* Extract:

  * `sender`, `subject`, `timestamp`, `content`, `attachments`.
* Store raw data temporarily before classification.

### 3. AI Categorization

* Call GPT-4 via OpenAI API:

  ```python
  prompt = f"""
  Categorize this hospital email into one of:
  ["Doctor / Patient Communication", "Diagnostic Results", "Insurance Claims", "Billing / Payment", "Appointment Confirmation", "Official Notice", "Report"].
  Email: {email_body}
  """
  ```
* Output JSON with: `category`, `summary`, `entities`, `priority`.

### 4. Entity Extraction

* Use hybrid approach:

  * Regex for invoice IDs, rupee values, dates.
  * LLM or spaCy for patient names, doctor names, etc.

### 5. Database Schema

```python
class EmailRecord(Base):
    __tablename__ = "emails"
    id = Column(String, primary_key=True)
    sender = Column(String)
    subject = Column(String)
    timestamp = Column(DateTime)
    category = Column(String)
    summary = Column(Text)
    content = Column(Text)
    entities = Column(JSON)
    attachments = Column(JSON)
```

### 6. RAG Query Endpoint

* Create `/query` API endpoint.
* Use LangChain + FAISS to embed email summaries.
* Let user ask:

  > “Show all billing emails from last 3 days.”
* Convert to SQL filter automatically.

### 7. Analytics API

* `/analytics/categories` → count by category
* `/analytics/trends` → daily trend data
* `/analytics/top-senders` → top sender list
* `/analytics/attachments` → type distribution

---

## 💻 Frontend Requirements (React)

### 1. Project Structure

```
frontend/
 ├── src/
 │   ├── components/
 │   │   ├── SummaryCards.jsx
 │   │   ├── TrendChart.jsx
 │   │   ├── TopSenders.jsx
 │   │   ├── AttachmentPie.jsx
 │   │   └── QueryPanel.jsx
 │   ├── pages/Dashboard.jsx
 │   ├── api/
 │   │   ├── analytics.js
 │   │   └── query.js
 │   └── App.jsx
 ├── package.json
 └── tailwind.config.js
```

### 2. Dashboard Design

* Filters: **Date Range**, **Category**
* Cards showing:

  * Doctor/Patient Communication count
  * Diagnostic Results count
  * Insurance Claims count
  * Billing/Payment count
* Trend chart: email volume by date
* Top senders bar chart
* Attachment distribution pie

### 3. RAG Query Panel

* Textbox + send button.
* User types: “Show insurance claim emails this week.”
* Call `/query` backend → render filtered cards.

---

## 🧠 AI Instructions for Copilot

When generating code, **always follow these principles**:

1. Use **async/await** for all I/O operations (FastAPI & Axios).
2. Use **TypeScript** for React components (if enabled).
3. Keep UI clean with **Tailwind CSS**.
4. Validate all inputs before DB insert.
5. Modularize LLM prompt templates under `/services/ai_categorizer.py`.
6. Use environment variables for API keys (`.env`).
7. Add docstrings for every function.
8. Write a minimal test suite (`pytest`) for backend APIs.
9. Include Dockerfile for both frontend & backend.

---

## 🧱 Database Example Queries

```sql
-- Get category distribution for past 3 days
SELECT category, COUNT(*) 
FROM emails 
WHERE timestamp > NOW() - INTERVAL '3 days'
GROUP BY category;

-- Get top senders
SELECT sender, COUNT(*) 
FROM emails 
GROUP BY sender 
ORDER BY COUNT(*) DESC 
LIMIT 5;
```

---

## ⚙️ Environment Variables (.env)

```
OPENAI_API_KEY=your-key
GMAIL_CLIENT_ID=your-client-id
GMAIL_CLIENT_SECRET=your-client-secret
DATABASE_URL=postgresql://user:pass@localhost:5432/medmail
```

---

## 🐳 Docker Setup

**Backend Dockerfile:**

```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Frontend Dockerfile:**

```dockerfile
FROM node:20
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["npm", "start"]
```

---

## ✅ Deliverables

Copilot should produce:

* Working **FastAPI backend** with email categorization + analytics endpoints.
* React **dashboard UI** with charts, filters, and AI query bar.
* Dockerized environment for deployment.
* Documented code (auto-generated API docs via Swagger).

---

## 🧭 Optional Extensions for Copilot

* Add **Auth0 / Firebase** for login.
* Add **export to CSV** for analytics.
* Add **real-time refresh** using WebSockets.
* Add **auto summary preview** for each email.

---