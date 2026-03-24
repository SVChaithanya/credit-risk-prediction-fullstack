# 🏦 Credit Risk Prediction System

An AI-powered loan risk assessment web application built with **FastAPI**, **LightGBM**, **PostgreSQL**, and a pure HTML/CSS/JS frontend.

---

## 📌 Project Overview

This system predicts whether a loan applicant is a **credit risk** using a trained machine learning model. It provides:

- Probability of Default (PD)
- Adjusted PD
- Expected Loss
- Monthly EMI
- Affordability Ratio
- Final Decision: **Accept** or **Reject**

---

## 🗂️ Project Structure

```
web/
├── main.py                  # FastAPI app entry point
├── db.py                    # Database connection & session
├── models.py                # SQLAlchemy ORM models
├── schemas.py               # Pydantic request schemas
├── auth.py                  # JWT auth, password hashing, token utils
├── email_utils.py           # Email sending utility (fastapi-mail)
├── model.pkl                # Trained LightGBM pipeline
├── features.pkl             # Feature list for ML model
├── .env                     # Environment variables (not committed)
├── requirements.txt         # Python dependencies
│
├── router/
│   ├── reg.py               # Registration endpoint
│   ├── verify.py            # Email verification endpoint
│   ├── login.py             # Login endpoint
│   └── loan.py              # Loan risk prediction endpoint
│
├── ml.py                    # ML model training script
│
└── frontend/
    ├── home.html            # Landing page
    ├── reg.html             # Registration page
    ├── verify.html          # Verification page (shows Customer ID)
    ├── login.html           # Login page
    └── loan.html            # Loan assessment form + results
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python) |
| ML Model | LightGBM + Scikit-learn Pipeline |
| Database | PostgreSQL + SQLAlchemy |
| Auth | JWT (Access + Refresh Tokens) |
| Email | fastapi-mail (SMTP) |
| Frontend | HTML + CSS + Vanilla JavaScript |

---

## 🧠 ML Model

Trained on the **Lending Club loan dataset** using a LightGBM classifier.

**Features used:**

| Feature | Description |
|---|---|
| `loan_amnt` | Requested loan amount |
| `annual_inc` | Annual income of applicant |
| `dti` | Debt-to-income ratio |
| `fico_mean` | Average FICO credit score |
| `int_rate` | Interest rate (%) |
| `term` | Loan term (36 or 60 months) |
| `grade` | Loan grade (A–G) |
| `purpose` | Purpose of the loan |

**Target:** Binary — `1` = Bad loan (Default/Charged Off), `0` = Good loan

**Metric:** ROC-AUC Score

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/credit-risk-prediction.git
cd credit-risk-prediction
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://username:password@localhost/dbname
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_FROM=your_email@gmail.com
SECRET_KEY=your_jwt_secret_key
```

> ⚠️ Never commit your `.env` file. It is listed in `.gitignore`.

### 4. Set Up the Database

Make sure PostgreSQL is running, then run:

```bash
python models.py
```

This auto-creates all tables via SQLAlchemy.

If the `risk` table is missing the `customer_id` column, run this SQL:

```sql
ALTER TABLE risk ADD COLUMN customer_id INTEGER;
ALTER TABLE risk ADD CONSTRAINT uq_risk_customer_id UNIQUE (customer_id);
```

### 5. Train the ML Model

```bash
python ml.py
```

This generates `model.pkl` and `features.pkl` in the root directory.

### 6. Start the Backend

```bash
uvicorn main:app --reload
```

Backend runs at: `http://localhost:8000`

API docs available at: `http://localhost:8000/docs`

### 7. Serve the Frontend

```bash
python -m http.server 5500
```

Open `http://localhost:5500/home.html` in your browser.

---

## 🔐 API Endpoints

### Auth

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register new user |
| POST | `/auth/verify` | Verify account with token |
| POST | `/auth/login` | Login with Customer ID + password |

### Loan

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/loan/` | Submit loan for risk assessment | ✅ Bearer Token |

---

## 🖥️ Frontend Flow

```
home.html
   │
   ├── reg.html        → Register → Token shown on screen (60s countdown)
   │                                + Token sent to email
   │
   ├── verify.html     → Paste token → Account activated → Customer ID shown
   │
   ├── login.html      → Login with Customer ID + password
   │                     (Customer ID auto-filled from previous step)
   │
   └── loan.html       → Fill loan details → Get AI risk assessment result
```

---

## 📊 Loan Assessment Response

```json
{
  "pd": 0.23,
  "adjusted_pd": 0.245,
  "expected_loss": 12250.00,
  "emi": 1652.73,
  "affordability_ratio": 0.33,
  "decision": "accept",
  "risk_level": "low"
}
```

### Decision Logic

| Condition | Decision |
|---|---|
| `affordability_ratio ≤ purpose_cap` AND `adjusted_pd ≤ 0.30` | ✅ Accept |
| Otherwise | ❌ Reject |

---

## 📦 Requirements

```
fastapi
uvicorn
sqlalchemy
psycopg2-binary
python-dotenv
passlib[bcrypt]
python-jose[cryptography]
fastapi-mail
lightgbm
scikit-learn
pandas
numpy
joblib
pydantic[email]
```

Generate with:

```bash
pip freeze > requirements.txt
```

---

## 🔒 Security Notes

- Passwords are hashed using **bcrypt**
- Authentication uses **JWT** (access + refresh tokens)
- CORS is enabled for all origins (restrict in production)
- Never expose your `.env` file

---

## 📁 .gitignore

Make sure your `.gitignore` includes:

```
.env
*.pkl
__pycache__/
*.pyc
loan.csv
venv/
```

---

## 👨‍💻 Author

**Surya** — [GitHub](https://github.com/SVChaithanya/Fullstack_Credit-Risk-Prediction)

---

## 📄 License

This project is for educational purposes.
