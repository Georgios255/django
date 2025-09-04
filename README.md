## Project overview

Employee Management System built with **Django + DRF** on **PostgreSQL**.

- Models: **Department**, **Employee**, **Attendance**, **Performance**
- APIs: Full CRUD with **pagination**, **search**, **ordering**, and **filtering**
- Auth: **JWT (SimpleJWT)**
- Docs: **Swagger UI** at `/swagger/`
- Seed data: Management command with **Faker**

---

## Setup

### Prereqs
- Python 3.11+  
- PostgreSQL 14+ (or use Docker)      
- Git

### 1) Clone & create virtualenv
Windows (PowerShell)

git clone <YOUR_REPO_URL>    
cd <YOUR_REPO_FOLDER>    
python -m venv .venv    
.\.venv\Scripts\activate   

macOS/Linux   
 
git clone <YOUR_REPO_URL>    
cd <YOUR_REPO_FOLDER>    
python3 -m venv .venv     
source .venv/bin/activate   

### 2) Install dependencies

pip install -r requirements.txt

### 3) Configure environment
Copy the example and edit values as needed:

Windows   
powershell    
copy .env.example .env   

macOS/Linux    

cp .env.example .env      

.env example   

DEBUG=True    
SECRET_KEY=change-me    
ALLOWED_HOSTS=127.0.0.1,localhost,0.0.0.0     

DB_NAME=ems     
DB_USER=ems_user      
DB_PASSWORD=StrongPass!234     
DB_HOST=127.0.0.1    
DB_PORT=5432      

### 4) Create database & user in Postgres

CREATE USER ems_user WITH PASSWORD 'StrongPass!234';    
CREATE DATABASE ems OWNER ems_user;    
GRANT ALL PRIVILEGES ON DATABASE ems TO ems_user;

### 5) Migrate, create admin, and seed data
  
python manage.py migrate    
python manage.py createsuperuser    
python manage.py seed_data --employees 50   

### 6) Run the server

python manage.py runserver   
Swagger: http://127.0.0.1:8000/swagger/   
Admin: http://127.0.0.1:8000/admin/

### Docker (optional)
If you have Dockerfile and docker-compose.yml:  
     
docker compose up --build
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py seed_data --employees 50
Then open http://localhost:8000/swagger/.

## API usage guide

### Authentication (JWT)

Get access/refresh tokens   

curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"<your_user>","password":"<your_pass>"}'

Response   
 
{ "access": "<ACCESS>", "refresh": "<REFRESH>" }

Use the access token (header on all requests)
Authorization: Bearer <ACCESS>

Refresh the access token   
 
curl -X POST http://127.0.0.1:8000/api/token/refresh/ \   
  -H "Content-Type: application/json" \    
  -d '{"refresh":"<REFRESH>"}'   

In Swagger (/swagger/), click Authorize and paste:
Bearer <ACCESS>

### Common query parameters
Pagination: ?page=2    
Search: ?search=john (e.g., employee name/email)             
Ordering: ?ordering=field or ?ordering=-field (e.g., -date_of_joining)

### Departments

List   

curl -H "Authorization: Bearer <ACCESS>" \
  http://127.0.0.1:8000/api/departments/

Create   
  
curl -X POST http://127.0.0.1:8000/api/departments/ \
  -H "Authorization: Bearer <ACCESS>" -H "Content-Type: application/json" \  
  -d '{ "name": "Engineering" }'

Detail / Update / Delete    
GET/PUT/PATCH/DELETE /api/departments/{id}/    

### Employees

List with filters   

by department, joined_after, search, ordering   
curl -H "Authorization: Bearer <ACCESS>" \
  "http://127.0.0.1:8000/api/employees/?department=1&joined_after=2024-01-01&search=john&ordering=-date_of_joining"

Create    
  
curl -X POST http://127.0.0.1:8000/api/employees/ \
  -H "Authorization: Bearer <ACCESS>" -H "Content-Type: application/json" \
  -d '{   
        "name": "Jane Smith",   
        "email": "jane@example.com",   
        "phone": "+1 555 000 1234",   
        "address": "123 Main St",   
        "date_of_joining": "2024-07-15",   
        "department_id": 1   
      }'

Detail / Update / Delete
GET/PUT/PATCH/DELETE /api/employees/{id}/

### Attendance

List with filters

curl -H "Authorization: Bearer <ACCESS>" \
  "http://127.0.0.1:8000/api/attendance/?employee=1&status=P&date_from=2024-01-01&date_to=2024-12-31&ordering=-date"

CRUD  
 
POST/GET/PUT/PATCH/DELETE /api/attendance/                       
fields: employee (id), date (YYYY-MM-DD), status (P|A|L)

### Performance

List with filters    
 
curl -H "Authorization: Bearer <ACCESS>" \
  "http://127.0.0.1:8000/api/performances/?employee=1&rating=5&review_date_from=2024-01-01&ordering=-review_date"

CRUD    
POST/GET/PUT/PATCH/DELETE /api/performances/      
fields: employee (id), rating (1-5), review_date (YYYY-MM-DD)

### Tips
401 errors? Re-fetch a fresh access token and re-Authorize in Swagger.

Adjust page size/search/ordering in DRF settings if needed.