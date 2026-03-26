# Credit Risk Prediction — Full Stack

Full-stack credit risk assessment app — FastAPI backend + PostgreSQL + complete frontend UI.

> Backend-only version (no frontend, no auth): [credit_risk_prediction](https://github.com/SVChaithanya/credit_risk_prediction)

---

## Tech Stack

- FastAPI
- LightGBM
- PostgreSQL
- SQLAlchemy
- Pydantic v2
- HTML / CSS / JS (Frontend)

---

## Project Structure
```
credit_risk_prediction_fullstack/
├── backend/    → FastAPI + LightGBM + PostgreSQL
└── frontend/   → Full UI (results page, risk display, EMI breakdown)
```

---

## What It Does

User fills a loan application form → backend runs ML inference → frontend displays:

- Approved or Rejected
- Risk Level (Low / Medium / High)
- Prediction score (probability of default)
- EMI calculation based on loan amount + term
- Full decision breakdown

---

## System Design Highlights

### Backend (`/backend`)

- Loan application validation via Pydantic v2 (8 input fields, field-level error responses)
- LightGBM inference with business rules pipeline:
  - EMI-to-income cap (≤40%)
  - Purpose-based loan ceilings
  - Grade + term risk multipliers
  - Adjusted PD threshold at 0.30
- PostgreSQL storage via SQLAlchemy ORM (prediction + audit_log in atomic transaction)
- Latency: ~45ms avg after moving model load to startup lifespan event (was ~380ms)
- Rate limiting via Slowapi (10 req/min per IP)

---

### Frontend (`/frontend`)

- Approval/rejection status with visual indicator
- Risk level badge (Low / Medium / High)
- Predicted probability of default
- EMI amount calculated from loan inputs
- Clean form for submitting new applications

> Frontend was scaffolded using an AI tool (Claude) based on my UI design spec.
> Backend logic, ML integration, and DB layer are entirely my own work.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /predict | Submit application, get full prediction response |
| GET | /health | Health check |

---

## Sample Response
```json
{
  "decision": "Approved",
  "risk_level": "Medium",
  "probability_of_default": 0.27,
  "emi": 4850.00,
  "adjusted_pd": 0.27,
  "message": "Application meets threshold criteria"
}
```

---

## Local Setup

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
python -m http.server 3000
```

Swagger UI: http://localhost:8000/docs

---

## Deployment

- Backend: deploying to Render (in progress)
- Frontend: deploying to Render static site (in progress)
- Docker setup: in progress

---

## Known Limitations

- Rate limiting is in-memory — breaks under horizontal scaling (needs Redis)
- No user authentication on this version
- Concurrency not load tested beyond 50 threads on a single machine
- Frontend scaffolded with AI tooling — not hand-written CSS/JS
