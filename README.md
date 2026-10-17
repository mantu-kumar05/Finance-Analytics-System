# Finance Analytics System

A Python-based financial management and analytics system that tracks income and expenses, provides REST APIs, performs financial analysis, and generates visualization reports.

Built with **FastAPI**, **SQLite**, **Pandas**, **Matplotlib** and **Streamlit**, with JWT-based user authentication.

## Features

- User registration and login
- JWT authentication with protected REST APIs
- Add, view and delete financial transactions
- Total income, total expenses and savings per user
- Category-wise expense analysis
- Generated financial charts
- Interactive Streamlit dashboard
- SQLite database, created automatically on first run
- Automated API testing with Pytest

## Tech Stack

| Area | Technologies |
|---|---|
| Backend | Python, FastAPI, Pydantic, Uvicorn |
| Database | SQLite |
| Authentication | JWT, OAuth2 password flow, Passlib, Bcrypt |
| Data analysis | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn, Plotly |
| Dashboard | Streamlit |
| Testing | Pytest, FastAPI TestClient |

## Project Structure

```
Finance-Analytics-System/
├── app/
│   ├── main.py               # FastAPI routes
│   ├── models.py             # Request and response models
│   ├── database.py           # Database connection
│   ├── init_db.py            # Creates tables on startup
│   ├── crud.py               # Database CRUD operations
│   ├── analytics_service.py  # User-based analytics logic
│   ├── analytics.py          # Analytics helpers
│   ├── charts.py             # Chart generation
│   ├── users.py              # Register and login APIs
│   ├── auth.py               # JWT token creation
│   ├── config.py             # Settings (secret key)
│   ├── security.py           # Password hashing
│   ├── dependencies.py       # JWT authentication
│   ├── migrate.py            # Legacy migration script
│   ├── insert_data.py        # Sample data script
│   └── view_data.py          # Database viewer script
├── dashboard/
│   └── app.py                # Streamlit dashboard
├── charts/                   # Generated chart images
├── screenshots/              # README screenshots
├── tests/
│   └── test_api.py           # API tests
├── Procfile                  # Start command for hosting
└── requirements.txt
```

The `database/` folder and `finance.db` file are created automatically the first time the API starts.

## Installation and Setup

```
git clone https://github.com/mantu-kumar05/Finance-Analytics-System.git
cd Finance-Analytics-System
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Environment variables

| Variable | Used by | Default | Description |
|---|---|---|---|
| `SECRET_KEY` | API | `dev-only-change-me` | Key used to sign JWT tokens. Always set your own value outside local development. |
| `API_URL` | Dashboard | `http://127.0.0.1:8000` | Address of the FastAPI backend |

Example (Windows Command Prompt):

```
set SECRET_KEY=replace-with-a-long-random-string
```

### Run the API

```
uvicorn app.main:app --reload
```

- Server: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI: http://127.0.0.1:8000/openapi.json

### Run the dashboard

Open a second terminal, activate the virtual environment, and run:

```
streamlit run dashboard/app.py
```

Dashboard: http://localhost:8501

## Database Design

**users:** `user_id`, `name`, `email`, `password` (hashed)

**transactions:** `transaction_id`, `user_id`, `amount`, `category`, `transaction_type`, `transaction_date`

## API Reference

All transaction and analytics endpoints require a JWT token.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health message |
| POST | `/register` | Create a user |
| POST | `/login` | Log in and receive a token |
| GET | `/transactions` | List the logged-in user's transactions |
| POST | `/transactions` | Add a transaction |
| DELETE | `/transactions/{transaction_id}` | Delete a transaction |
| GET | `/analytics` | Income, expense and savings summary |

### Register

`POST /register`

```json
{
  "name": "Mantu Kumar",
  "email": "mantu@gmail.com",
  "password": "123456"
}
```

Response:

```json
{ "message": "User registered successfully" }
```

### Login

`POST /login`

Send `username` (the email) and `password` as **form data** (OAuth2 password flow). In Swagger UI, use the **Authorize** button.

Response:

```json
{
  "access_token": "your_token",
  "token_type": "bearer"
}
```

### Add a transaction

`POST /transactions`

```json
{
  "amount": 300,
  "category": "Shopping",
  "transaction_type": "Expense",
  "transaction_date": "2026-08-03"
}
```

`user_id` is taken from the JWT token automatically.

### Analytics

`GET /analytics`

```json
{
  "total_income": 2000,
  "total_expense": 1300,
  "savings": 700
}
```

## Streamlit Dashboard

The dashboard connects to the FastAPI backend and provides:

- Register and login tabs with JWT sessions
- Automatic logout when the session expires
- Total income, total expenses and savings
- Transactions table
- Add-transaction form with a date picker
- Expense category chart
- Clear messages when the API is not running

## Analytics and Visualization

The system generates a category-wise expense chart and an income vs expense chart, saved in the `charts/` folder.

## Running Tests

```
pytest
```

Current tests cover the home, transactions and analytics endpoints.

## Future Improvements

- Monthly financial reports
- Cloud database integration
- Docker deployment
- Machine learning based expense prediction

## Screenshots

### Login Page
![Login](screenshots/login.png)

### Finance Dashboard
![Dashboard](screenshots/dashboard.png)

### Expense Analysis
![Expense Analysis](screenshots/expense.png)

### Add Transaction
![Add Transaction](screenshots/add_transaction.png)

## Author

**Mantu Kumar**