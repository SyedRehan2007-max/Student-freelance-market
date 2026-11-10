# Student Freelance Marketplace
### Python Full Stack Development Internship Project

A simple, complete, and functional web-based freelance platform designed specifically for college students to earn money, showcase their skills, and gain industry experience, while allowing clients to post projects and hire young talent.

---

## Quick Start (Windows)

Open PowerShell in this folder:
```powershell
cd freelance_marketplace
python manage.py runserver
```
Visit: **http://127.0.0.1:8000/**

### Pre-loaded Test Accounts
- **Admin**: `admin` / `admin123`
- **Client**: `client_techcorp` / `password123`
- **Student**: `student_alex` / `password123`

To re-seed or reset sample data at any time:
```powershell
cd freelance_marketplace
python manage.py seed_data
```

To run the automated test suite (17 tests):
```powershell
cd freelance_marketplace
python manage.py test
```

Please see `freelance_marketplace/README.md` for full documentation.

