# LIS — Laboratory Information System

Django + SQLite web application for lab test requests, sample workflow, results, and reports.

## Prerequisites

- Python 3.10+
- pip

## Installation

```powershell
cd laboratory
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata fixtures\initial_data.json
python manage.py createsuperuser
python manage.py seed_demo_users
python manage.py runserver
```

`loaddata` installs **12** objects (2 test menus, 5 assays, 5 patients), not 15 — that number in some checklists is a typo.

If a Django user has no **User profile**, the first successful login **creates one automatically** (employee id `EMP-…`, role **Admin** for superusers, otherwise **Physician**). You can still edit the profile in **Admin → Users** (inline).

## Demo users (Step 1 — use this instead of manual shell)

```powershell
python manage.py seed_demo_users
```

Password for every demo user: **`Pass@1234`**

| Username        | Full name (profile) | Role            |
|----------------|----------------------|-----------------|
| `physician1`   | Dr. Ravi Kumar       | Physician       |
| `nurse1`       | Nurse Priya          | Nurse           |
| `phlebotomist1` | Sam Collector       | Phlebotomist    |
| `techlab1`     | Tech Arun            | LabTechnician   |

Your **superuser** (e.g. Adarsh) uses the **username and password you chose** for `createsuperuser`.

**Frontend permissions:** pages like `/patients/register/` are limited by role (e.g. a logged-in phlebotomist is sent back to the dashboard with an error — Step 11 in your checklist). **Admin** can still open any page for support/testing.

## URLs

- Frontend: http://127.0.0.1:8000/
- API: http://127.0.0.1:8000/api/v1/
- Admin: http://127.0.0.1:8000/admin/

## API quick reference

- `POST /api/v1/auth/login/` — JWT access + refresh
- `GET /api/v1/patients/` — list patients
- `POST /api/v1/orders/` — create order
- `PATCH /api/v1/orders/{id}/collect/` — collect sample
- `PATCH /api/v1/orders/{id}/receive/` — mark In-Lab
- `POST /api/v1/orders/{id}/results/` — enter results
- `GET /api/v1/orders/{id}/report/` — JSON lab report (completed orders)

## Notes

- Session-based UI uses Django login; the MRN refresh button calls `/ajax/generate-mrn/` (same session, no JWT in the browser).
- **API tests (curl):** On Windows PowerShell, use ``curl.exe`` or `$env:TOKEN="..."` instead of bash `TOKEN=...` syntax.
- `weasyprint` is listed for optional PDF export; PDF views are not wired in this scaffold.
