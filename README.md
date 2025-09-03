# Employee Management System (Django + DRF)

APIs for Employees, Departments, Attendance, Performance with JWT auth and Swagger docs.  
Optional: analytics endpoints + Chart.js page.

## Tech
- Django 4.x, DRF, django-filter, SimpleJWT, drf-yasg
- PostgreSQL
- Faker (seed data)

## Setup
```bash
git clone <your-repo-url>
cd PythonProject
python -m venv .venv && .\.venv\Scripts\activate  # win
# or source .venv/bin/activate on mac/linux
pip install -r requirements.txt
copy .env.example .env  # win; mac/linux: cp .env.example .env
# create DB/user in Postgres matching .env
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_data --employees 50
python manage.py runserver