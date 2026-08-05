# NMM Django Backend

Django REST API and admin dashboard for the NMM Student Expense Tracker app.

> Flutter frontend: [nmm-flutter-frontend](https://github.com/reaksa120906/nmm-flutter-frontend)

---

## Structure

```
NewDjango/
├── manage.py
├── Procfile                             # gunicorn entry point
├── requirements.txt
│
├── nmmApp/                              # Project config
│   ├── settings.py
│   ├── urls.py                          # Root URL routing
│   └── wsgi.py
│
├── api/                                 # Main app
│   ├── models.py                        # Expense, Income, Savings, UserProfile
│   ├── serializers.py
│   ├── views.py                         # JWT-protected REST API
│   ├── dashboard_views.py               # Admin dashboard (session auth)
│   ├── flutter_view.py                  # Serves Flutter web build at /app/
│   └── urls.py
│
└── templates/dashboard/
    ├── base.html                        # Layout shell (sidebar + topbar)
    ├── login.html                       # Admin login
    ├── index.html                       # Dashboard home
    ├── reports.html                     # Expenses table + delete
    ├── notifications.html               # Budget alerts + income summary
    ├── savings.html                     # Saving goals
    ├── profile.html                     # User management
    └── settings.html
```

---

## Running Locally

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

- Dashboard: `http://localhost:8000/dashboard/`
- API base:  `http://localhost:8000/api/`

To share on local network, your device IP is used instead of `localhost`.

---

## API Endpoints

| Method | Endpoint | Auth |
|--------|----------|------|
| POST | `/api/register/` | Public |
| POST | `/api/login/` | Public |
| GET/PATCH | `/api/profile/` | JWT |
| GET/POST | `/api/expenses/` | JWT |
| DELETE | `/api/expenses/<id>/` | JWT |
| GET/POST | `/api/income/` | JWT |
| DELETE | `/api/income/<id>/` | JWT |
| GET/POST | `/api/savings/` | JWT |
| DELETE | `/api/savings/<id>/` | JWT |

---

## Tech Stack

- Django 6 + Django REST Framework
- JWT auth via `djangorestframework-simplejwt`
- SQLite (local) 
- WhiteNoise for static files
- Chart.js for dashboard charts
