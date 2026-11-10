# Student Freelance Marketplace
## Complete Internship Review & Viva Preparation Guide

This guide is designed to help you confidently present and explain your Python Full Stack Development internship project during college reviews and viva examinations.

---

## 1. Project Introduction

**What is the Student Freelance Marketplace?**
The Student Freelance Marketplace is a web application that connects college students looking for part-time freelance opportunities with clients who need small, real-world projects completed. It provides students with practical industry experience, an avenue to earn income, and a platform to build a verified portfolio of work.

---

## 2. Project Objective

**Why was this project developed?**
1. **Bridging the Gap:** Students often lack prior industry work experience required for full-time jobs. This platform gives them hands-on exposure to real clients.
2. **Affordable Quality Work for Clients:** Startups, local businesses, and individuals can hire eager, skilled students at reasonable budgets.
3. **Demonstrating Full-Stack Python Competence:** To build a complete end-to-end web system demonstrating the standard Django MTV (Model-Template-View) pattern, relational database management with SQLite, user authentication, and responsive frontend design.

---

## 3. Technology Stack & Justification

| Technology | Why Was It Chosen? |
|---|---|
| **Python** | High readability, clean syntax, rapid development, and extensive standard library. |
| **Django** | Robust, secure, "batteries-included" web framework with built-in authentication, ORM, CSRF protection, and admin site. |
| **SQLite** | Serverless, zero-configuration relational database ideal for lightweight applications and development environments. |
| **HTML5 & CSS3** | Clean semantic structure and customized typography, spacing, and brand coloring. |
| **Bootstrap 5** | Responsive mobile-first grid system, prebuilt UI components (cards, badges, modals, navigation), eliminating heavy frontend frameworks. |
| **Vanilla JavaScript** | Adds intuitive client-side interactivity (password visibility toggle, confirmation alerts before project deletion or proposal acceptance) without unnecessary npm dependencies. |
| **Django Templates** | Server-side template rendering that directly binds backend data context to HTML, keeping the system unified and easy to explain. |

---

## 4. Database Models Explained

The database contains **three custom models** linked to Django's built-in `User` table:

### 1. `Profile` Model
- **Relationship:** `OneToOneField` with `User`.
- **Purpose:** Extends the user account to distinguish between `Student` and `Client` roles.
- **Key Fields:** `role` (Student/Client), `skills` (e.g. Python, Django, Figma), `bio` (self-summary), `education` (degree/college).

### 2. `Project` Model
- **Relationship:** `ForeignKey` with `User` (`client`).
- **Purpose:** Represents the freelance jobs posted by clients.
- **Key Fields:** `title`, `description`, `category` (Web Dev, Design, Content, etc.), `budget`, `deadline`, `status` (`Open`, `Assigned`, `Completed`, `Closed`), and `created_at`.

### 3. `Proposal` Model
- **Relationship:** `ForeignKey` with `Project` and `ForeignKey` with `User` (`student`).
- **Purpose:** Stores a student's bid for a specific project.
- **Key Fields:** `description` (pitch), `proposed_amount`, `estimated_days`, `status` (`Pending`, `Accepted`, `Rejected`), `created_at`.
- **Constraint:** `unique_together = ('project', 'student')` prevents multiple submissions for the same project by one student.

---

## 5. CRUD Operations (Project Model)

CRUD represents the four basic operations of persistent storage:

1. **Create:** A logged-in client posts a new project via `post_project` view and `ProjectForm`. The project is saved with status `Open`.
2. **Read:** Students browse open projects on `projects.html` with search and category filters; clients view their own posted projects on `my_projects.html`.
3. **Update:** A client edits project details (budget, description, deadline, or status) via `edit_project` view.
4. **Delete:** A client deletes their project via `delete_project` view after confirming with a JavaScript alert.

---

## 6. Authentication & User Roles

- **Django Built-in Auth:** Uses Django's `django.contrib.auth` which securely hashes passwords using PBKDF2 with SHA-256 (never storing plain text).
- **Registration:** Users choose their role (`Student` or `Client`) during registration. The system creates a `User` record and an associated `Profile` record in one step.
- **Role Isolation:** Custom Python decorators (`@student_required`, `@client_required`, `@admin_required`) ensure students cannot access client posting/editing pages and clients cannot submit proposals.

---

## 7. Project & Proposal Workflow

### Project Posting & Application Workflow:
1. Client logs in and navigates to **Post Project**.
2. Client enters title, description, category, budget, and deadline. Project status becomes `Open`.
3. Student logs in, navigates to **Browse Projects**, and filters by category or search term.
4. Student views project details and clicks **Submit Proposal**.
5. Student inputs their proposed price, estimated timeline in days, and pitch.
6. The proposal is saved with status `Pending`.

### Proposal Decision Workflow:
1. Client visits **My Projects** and clicks **Proposals** on their project.
2. Client reviews student applicants, their skillsets, and proposed bids.
3. When the client clicks **Accept**:
   - The selected proposal status updates to `Accepted`.
   - The project status changes from `Open` to `Assigned`.
   - All other pending proposals for that project are automatically set to `Rejected`.
4. If a client clicks **Reject**, only that specific proposal is marked as `Rejected`.

---

## 8. Django Architecture (MTV Pattern)

Django uses the **MTV (Model-Template-View)** pattern:

- **Model (`models.py`):** Defines the database structure and relationships using Python classes without writing raw SQL.
- **Template (`templates/`):** Contains HTML with Django Template Language (DTL) tags (`{{ variable }}`, `{% for %}`, `{% if %}`) to present data to the user.
- **View (`views.py`):** The business logic layer. Functions receive HTTP requests, fetch/update database records via Django ORM, and render the corresponding template.
- **URLs (`urls.py`):** Routes incoming browser URL paths to the matching view functions.
- **Forms (`forms.py`):** Handles form rendering, server-side data cleaning, and validation before saving to the database.

---

## 9. Top 15 Faculty Review / Viva Questions & Answers

### Q1: What is Django and why did you choose it for this project?
**Answer:** Django is a high-level, open-source Python web framework. We chose it because of its built-in features such as user authentication, an Object-Relational Mapper (ORM), an administration panel, and robust security against CSRF and SQL injection.

### Q2: What is the MTV architecture in Django?
**Answer:** MTV stands for Model, Template, and View:
- **Model:** Represents database tables.
- **Template:** Represents the frontend HTML interface.
- **View:** Contains the backend business logic connecting Models and Templates.

### Q3: How is user role separation achieved?
**Answer:** We extended Django's `User` model using a `Profile` model with a `OneToOneField`. The `Profile` has a `role` field (`Student` or `Client`). Custom view decorators verify this role before granting access to protected views.

### Q4: How do you prevent plain-text passwords from being stored?
**Answer:** Django automatically hashes passwords using PBKDF2 with SHA-256 hashing and salts through the `make_password()` algorithm when `user.set_password()` or `User.objects.create_user()` is called.

### Q5: How do you prevent a student from submitting multiple proposals for the same project?
**Answer:** Two levels:
1. In the database: `unique_together = ('project', 'student')` inside `Proposal.Meta`.
2. In the view logic: We query if an existing proposal exists before saving and redirect with a warning if found.

### Q6: What is Django ORM and what are its advantages?
**Answer:** ORM stands for Object-Relational Mapping. It allows developers to interact with the database using Python objects and methods (e.g. `Project.objects.filter(status='Open')`) instead of writing raw SQL queries.

### Q7: What happens when a client accepts a student's proposal?
**Answer:** Three database changes happen simultaneously:
1. The chosen proposal's status is set to `Accepted`.
2. The project's status changes from `Open` to `Assigned`.
3. All other pending proposals for that project are automatically marked as `Rejected`.

### Q8: What validation rules are implemented for projects and proposals?
**Answer:**
- Budget and proposed amount must be greater than zero.
- Estimated completion days must be a positive integer.
- The project deadline cannot be in the past.
- Only users with the `Student` role can submit proposals.

### Q9: What is CSRF and how is it prevented in your project?
**Answer:** CSRF stands for Cross-Site Request Forgery. Django provides built-in protection via `CsrfViewMiddleware` and requires the `{% csrf_token %}` tag inside every HTML form that uses the POST method.

### Q10: Why did you use SQLite instead of MySQL or PostgreSQL?
**Answer:** SQLite is built directly into Python, requires zero setup or server configuration, stores data in a single local file (`db.sqlite3`), and is fast and lightweight for development and college project demonstration.

### Q11: How does the project search and category filter work?
**Answer:** In `views.py`, the `projects_list` view checks `request.GET.get('q')` and `request.GET.get('category')`. It uses Django's `Q` object to perform case-insensitive queries (`title__icontains=query`) and filters by category.

### Q12: Are the dashboard statistics hardcoded?
**Answer:** No. All numbers on both the Student and Client dashboards are calculated dynamically from the database using Django ORM count queries like `Proposal.objects.filter(student=request.user).count()`.

### Q13: Where is JavaScript used in this project?
**Answer:** JavaScript is used for client-side interactivity:
1. Toggling password visibility (show/hide).
2. Confirmation alerts before deleting a project or accepting a proposal.
3. Auto-dismissing alert notifications after 5 seconds.

### Q14: How does Django handle template inheritance?
**Answer:** We created a master `base.html` containing the navigation bar, Bootstrap links, alerts, and footer. All other pages use `{% extends 'marketplace/base.html' %}` and place their page-specific content inside `{% block content %}`.

### Q15: How can a reviewer verify that the project is working?
**Answer:** We built an automated test suite containing 17 unit tests in `marketplace/tests.py`. Running `python manage.py test` executes tests covering registration, login, role restrictions, project CRUD, proposal workflow, and security checks.

