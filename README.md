# LIS — Laboratory Information System

A web-based Laboratory Information System built with Django, Django REST Framework, and SQLite. Covers the full lifecycle of lab test requests — from patient registration through sample collection, result entry, and report generation — with role-based access for 5 user types.

## Tech Stack

- **Backend:** Django (Python)
- **API:** Django REST Framework + JWT
- **Database:** SQLite
- **Frontend:** Django Templates + Bootstrap 5

## User Roles

| Role | Access |
|---|---|
| Admin | Full access |
| Physician | Register patients, place orders, view reports |
| Nurse | Place orders, view reports |
| Phlebotomist | Collect samples |
| Lab Technician | Enter results, complete orders |

## Prerequisites

- Python 3.10+
- pip

## Installation

```bash
git clone https://github.com/Adarshmanojk/lis-django.git
cd lis-django

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt

copy .env.example .env       # Windows
# cp .env.example .env       # Mac/Linux

python manage.py migrate
python manage.py loaddata fixtures/initial_data.json
python manage.py createsuperuser
python manage.py runserver
```

## Create Demo Users (after runserver)

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from accounts.models import UserProfile

users = [
    ('physician1', 'Dr. Ravi Kumar', 'Physician', 'EMP001', 'Senior Physician', 'Pathology'),
    ('nurse1', 'Nurse Priya', 'Nurse', 'EMP002', 'Staff Nurse', 'Ward'),
    ('phlebotomist1', 'Sam Collector', 'Phlebotomist', 'EMP003', 'Phlebotomist', 'Lab'),
    ('techlab1', 'Tech Arun', 'LabTechnician', 'EMP004', 'Lab Technician', 'Pathology'),
]
for username, full_name, role, emp_id, designation, dept in users:
    u = User.objects.create_user(username=username, password='Pass@1234')
    UserProfile.objects.create(user=u, employee_id=emp_id, full_name=full_name,
        role=role, designation=designation, department=dept, status='Active')
    print(f'Created: {username}')
```

## Access

| URL | Purpose |
|---|---|
| http://localhost:8000/ | Frontend |
| http://localhost:8000/admin/ | Django Admin |
| http://localhost:8000/api/v1/ | REST API |

## API Quick Reference

```
POST   /api/v1/auth/login/              — Get JWT tokens
POST   /api/v1/auth/logout/             — Logout
GET    /api/v1/patients/                — List patients
POST   /api/v1/patients/                — Create patient
GET    /api/v1/tests/assays/            — List assays
POST   /api/v1/orders/                  — Create order
PATCH  /api/v1/orders/{id}/collect/     — Collect sample
PATCH  /api/v1/orders/{id}/receive/     — Mark In-Lab
POST   /api/v1/orders/{id}/results/     — Enter results
GET    /api/v1/orders/{id}/report/      — Get lab report
```

## Order Status Workflow

```
Ordered (1) → Collected (2) → In-Lab (3) → Completed (4)
```

## Default Test Credentials

| Username | Password | Role |
|---|---|---|
| physician1 | Pass@1234 | Physician |
| nurse1 | Pass@1234 | Nurse |
| phlebotomist1 | Pass@1234 | Phlebotomist |
| techlab1 | Pass@1234 | Lab Technician |