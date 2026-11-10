# Student Freelance Marketplace
### Python Full Stack Development Internship Project

A simple, complete, and functional web-based freelance platform designed specifically for college students to earn money, showcase their skills, and gain industry experience, while allowing clients to post projects and hire young talent.

---

## 1. Project Overview

The **Student Freelance Marketplace** connects college student freelancers with clients who have freelance requirements (such as web development, graphic design, content writing, video editing, etc.). 

- **Students** can build rich profiles, browse open projects, search/filter by category, submit proposals with custom quotes and timelines, and track proposal statuses.
- **Clients** can register, post projects with budgets and deadlines, manage their projects (Create, Read, Update, Delete), review student proposals, and accept or reject candidates.
- **Administrators** can view platform-wide analytics and manage all database records via Django's secure built-in Admin panel.

---

## 2. Project Objective

The primary objective is to demonstrate the fundamentals of full-stack Python development using Django's **Model-Template-View (MTV)** architecture. The project illustrates:
- Backend logic and database connectivity with **SQLite**.
- User authentication and role-based access control (**Student**, **Client**, and **Admin**).
- Full **CRUD** (Create, Read, Update, Delete) operations.
- Dynamic data rendering with **Django Templates**.
- Responsive UI using **HTML5**, **CSS3**, and **Bootstrap 5**.
- Basic client-side interactivity using **vanilla JavaScript**.

---

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| **Python 3.x** | Backend programming language |
| **Django 5.x / 6.x** | High-level Python web framework |
| **SQLite3** | Lightweight, relational SQL database (file-based) |
| **HTML5 & CSS3** | Web structure and custom design styling |
| **Bootstrap 5** | Responsive layout, grid system, and UI components |
| **Vanilla JavaScript** | Form validation, password visibility toggle, confirmation alerts |
| **Django Templates** | Server-side template rendering with MTV pattern |

---

## 4. Main Features

### Student / Freelancer
- **Registration & Authentication:** Secure signup with role selection (`Student`), password hashing, and login/logout.
- **Student Profile:** Showcase full name, email, education, technical skills, and a short biography. Editable anytime.
- **Browse & Search Projects:** Filter open projects by category or search by keywords.
- **Submit Proposals:** Submit bids specifying proposed amount, completion timeline (days), and an introductory pitch.
- **Prevent Duplicate Proposals:** System ensures students can only submit one proposal per project.
- **My Proposals Tracker:** View all submitted proposals with live status badges (`Pending`, `Accepted`, `Rejected`).
- **Student Dashboard:** Dynamic statistics tracking submitted proposals, pending reviews, accepted gigs, and newly available projects.

### Client / Project Poster
- **Client Registration & Login:** Direct signup as `Client`.
- **Project CRUD Operations:**
  - **Create:** Post projects with title, description, category, budget, and deadline.
  - **Read:** View active projects and proposals received.
  - **Update:** Edit requirements, budget, or timeline.
  - **Delete:** Remove projects with client-side JavaScript confirmation.
- **Proposal Review & Decision:** Review student profiles, skills, and bids. Accept a student (which automatically marks the project as `Assigned` and notifies other applicants) or reject proposals.
- **Client Dashboard:** Real-time statistics displaying total projects posted, open projects, completed projects, and total proposals received.

### Administrator
- **Admin Dashboard:** High-level platform statistics (Total Students, Total Clients, Total Projects, Total Proposals).
- **Django Admin Interface:** Full database control at `/admin/` with search filters and date hierarchies.

---

## 5. Database Structure

The project implements **three clean custom models** linked to Django's built-in `User` model:

### 1. `Profile` Model
| Field | Type | Description |
|---|---|---|
| `id` | AutoField | Primary Key |
| `user` | OneToOneField (User) | Connects to Django auth User |
| `role` | CharField | `Student` or `Client` |
| `skills` | TextField | Comma-separated list of skills |
| `bio` | TextField | Short self-introduction |
| `education` | CharField | College / Degree information |

### 2. `Project` Model
| Field | Type | Description |
|---|---|---|
| `id` | AutoField | Primary Key |
| `client` | ForeignKey (User) | Client who posted the project |
| `title` | CharField | Project headline (max 200 chars) |
| `description` | TextField | Requirements and deliverables |
| `category` | CharField | Category (Web Dev, Design, Writing, etc.) |
| `budget` | DecimalField | Project budget in ₹ |
| `deadline` | DateField | Submission deadline |
| `status` | CharField | `Open`, `Assigned`, `Completed`, `Closed` |
| `created_at` | DateTimeField | Timestamp of creation |

### 3. `Proposal` Model
| Field | Type | Description |
|---|---|---|
| `id` | AutoField | Primary Key |
| `project` | ForeignKey (Project) | Related project |
| `student` | ForeignKey (User) | Student freelancer submitting proposal |
| `description` | TextField | Pitch / proposal cover letter |
| `proposed_amount` | DecimalField | Student's requested price in ₹ |
| `estimated_days` | PositiveIntegerField | Estimated turnaround in days |
| `status` | CharField | `Pending`, `Accepted`, `Rejected` |
| `created_at` | DateTimeField | Submission timestamp |

*Note: `unique_together = ('project', 'student')` prevents duplicate proposals.*

---

## 6. Project Folder Structure

```text
freelance_marketplace/
│
├── manage.py                          # Django command-line execution utility
├── db.sqlite3                         # SQLite database file
│
├── freelance_marketplace/             # Project Configuration Package
│   ├── __init__.py
│   ├── settings.py                    # Installed apps, templates, database, auth
│   ├── urls.py                        # Root URL routing
│   ├── wsgi.py                        # Web Server Gateway Interface
│   └── asgi.py                        # Asynchronous Server Gateway Interface
│
└── marketplace/                       # Main Django Application
    ├── __init__.py
    ├── admin.py                       # Model registration in Django Admin
    ├── apps.py                        # App configuration
    ├── forms.py                       # Registration, Login, Project, Proposal forms
    ├── models.py                      # Profile, Project, Proposal models
    ├── views.py                       # Function-based views for Student, Client, Admin
    ├── urls.py                        # Application URLs
    ├── tests.py                       # 17 automated unit tests
    │
    ├── migrations/                    # Database migration files
    │   └── 0001_initial.py
    │
    ├── management/commands/           # Management commands
    │   └── seed_data.py               # Populates sample data
    │
    ├── templates/marketplace/         # HTML Templates
    │   ├── base.html                  # Base layout with navbar, footer & alerts
    │   ├── home.html                  # Landing page (Hero, Categories, Featured)
    │   ├── login.html                 # Sign In page with show/hide password
    │   ├── register.html              # Sign Up page (Student & Client)
    │   ├── projects.html              # Browse & filter open projects
    │   ├── project_detail.html        # Detailed view of a project
    │   ├── student_dashboard.html     # Student metrics & open gigs
    │   ├── student_profile.html       # Public/personal profile view
    │   ├── edit_profile.html          # Edit skills, bio, education
    │   ├── submit_proposal.html       # Proposal submission form
    │   ├── my_proposals.html          # List of student's submitted proposals
    │   ├── client_dashboard.html      # Client metrics & project overview
    │   ├── post_project.html          # Project creation form
    │   ├── my_projects.html           # Client project management (CRUD)
    │   ├── edit_project.html          # Project edit form
    │   ├── view_proposals.html        # Review & accept/reject student proposals
    │   └── admin_dashboard.html       # Admin summary & platform metrics
    │
    └── static/marketplace/            # Static Assets
        ├── css/
        │   └── style.css              # Custom styling & Indigo color palette
        └── js/
            └── script.js              # Password toggle, confirm modals, alerts
```

---

## 7. Installation & Setup Instructions

Follow these exact steps to run the application on your local computer.

### Step 1: Open Terminal / PowerShell
Open your terminal in the project directory:
```bash
cd "c:\Users\hp\Desktop\Internship project\freelance_marketplace"
```

### Step 2: (Optional) Create & Activate Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Django
```bash
pip install django
```

### Step 4: Apply Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Populate Realistic Sample Data (Recommended)
We have included a built-in seeding command that automatically creates sample clients, students, projects, and proposals:
```bash
python manage.py seed_data
```

### Step 6: Create Admin Superuser (Manual alternative)
If you wish to create your own admin account manually:
```bash
python manage.py createsuperuser
```
Follow the prompts to enter username, email, and password.

### Step 7: Run Automated Unit Tests
Verify that all 17 system and security tests pass:
```bash
python manage.py test
```

### Step 8: Start the Local Development Server
```bash
python manage.py runserver
```

Open your web browser and visit:
- **Website Homepage:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Django Admin Panel:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **Custom Admin Dashboard:** [http://127.0.0.1:8000/admin-dashboard/](http://127.0.0.1:8000/admin-dashboard/)

---

## 8. Ready-to-Use Sample Login Credentials

When using `python manage.py seed_data`, you can test all roles immediately:

| Role | Username | Password | Notes |
|---|---|---|---|
| **Administrator** | `admin` | `admin123` | Full access to Admin Panel & custom dashboard |
| **Client 1** | `client_techcorp` | `password123` | Has 3 posted projects & received proposals |
| **Client 2** | `client_startup` | `password123` | Has 3 posted projects & received proposals |
| **Student 1** | `student_alex` | `password123` | Python/Django developer; 1 accepted proposal |
| **Student 2** | `student_priya` | `password123` | UI/UX & Graphic designer |
| **Student 3** | `student_rahul` | `password123` | Technical Content writer |

