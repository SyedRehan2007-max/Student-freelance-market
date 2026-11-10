# STUDENT FREELANCE MARKETPLACE
## Academic Internship Project Report & Technical Specification Document

**Project Title:** Student Freelance Marketplace  
**Domain:** Python Full Stack Web Development  
**Framework:** Django (MTV Architecture)  
**Database:** SQLite3  
**Frontend:** HTML5, CSS3, Bootstrap 5, Vanilla JavaScript  
**Author / Student:** Python Full Stack Development Intern  

---

## 1. Abstract

The **Student Freelance Marketplace** is a web-based platform tailored for university and college students seeking real-world freelancing engagements and practical industry experience. The platform bridges the experience gap by connecting students who possess emerging digital skills (such as Web Development, Graphic Design, Content Writing, and UI/UX) with clients seeking affordable and flexible task execution.

The system is constructed using the Python Django framework following the **Model-Template-View (MTV)** software design pattern. It integrates user authentication, role-based authorization (Student vs. Client vs. Administrator), full database CRUD (Create, Read, Update, Delete) capability on project records, and a proposal submission and evaluation lifecycle. Client-side enhancements include dynamic form validation, password visibility toggles, and modal confirmations built using lightweight vanilla JavaScript.

---

## 2. System Requirements Specification

### 2.1 Hardware Requirements
- **Processor:** Dual-core 2.0 GHz or higher (Intel Core i3/i5/i7 or AMD Ryzen equivalent).
- **RAM:** Minimum 4 GB (8 GB recommended).
- **Storage:** Minimum 500 MB free hard drive space.
- **Display Resolution:** 1280 x 720 minimum (optimized for 1920 x 1080 and mobile screens).

### 2.2 Software Requirements
- **Operating System:** Windows 10/11, macOS, or Linux.
- **Language / Runtime:** Python 3.10 - 3.14.
- **Web Framework:** Django 5.x / 6.x.
- **Database:** SQLite 3 (built into Python standard library).
- **Web Browser:** Google Chrome, Mozilla Firefox, Microsoft Edge, or Safari.
- **Code Editor / IDE:** Visual Studio Code, Antigravity IDE, or PyCharm.

---

## 3. System Architecture & Design

### 3.1 Django MTV Architecture
```
                        HTTP Request
                             │
                             ▼
                     ┌───────────────┐
                     │    urls.py    │ (URL Dispatcher)
                     └───────┬───────┘
                             │ Routes to matching view
                             ▼
                     ┌───────────────┐
                     │   views.py    │ (Business Logic Layer)
                     └───┬───────┬───┘
                         │       │
       Queries / Updates │       │ Renders context data
                         ▼       ▼
      ┌────────────────────┐   ┌────────────────────┐
      │     models.py      │   │    templates/      │
      │    (Database)      │   │   (HTML/CSS/JS)    │
      └─────────┬──────────┘   └─────────┬──────────┘
                │                        │
                ▼                        ▼
           db.sqlite3               HTTP Response
                                 (Rendered HTML page)
```

### 3.2 Entity-Relationship (ER) Diagram

```text
    ┌───────────────────────────┐
    │     auth_user (User)      │
    ├───────────────────────────┤
    │ PK id                     │
    │    username               │
    │    email                  │
    │    first_name             │
    │    last_name              │
    │    password (hashed)      │
    └─────┬──────────────┬──────┘
          │ 1            │ 1
          │              │
          │ 1            │ *
    ┌─────▼─────────┐  ┌─▼──────────────────────┐
    │    Profile    │  │        Project         │
    ├───────────────┤  ├────────────────────────┤
    │ PK id         │  │ PK id                  │
    │ FK user_id ───┘  │ FK client_id ──────────┘
    │    role          │    title               │
    │    skills        │    description         │
    │    bio           │    category            │
    │    education     │    budget              │
    └───────────────┘  │    deadline            │
                       │    status              │
                       │    created_at          │
                       └─────────┬──────────────┘
                                 │ 1
                                 │
                                 │ *
                       ┌─────────▼──────────────┐
                       │        Proposal        │
                       ├────────────────────────┤
                       │ PK id                  │
                       │ FK project_id ─────────┘
                       │ FK student_id (User)
                       │    description (pitch) │
                       │    proposed_amount     │
                       │    estimated_days      │
                       │    status              │
                       │    created_at          │
                       │                        │
                       │ CONSTRAINT:            │
                       │ unique_together =      │
                       │ ('project', 'student') │
                       └────────────────────────┘
```

---

## 4. Data Flow & Lifecycle Walkthrough

### 4.1 Project Posting (Client)
1. The client navigates to `/projects/post/`.
2. Client submits the `ProjectForm` with title, category, budget, deadline, and description.
3. `views.post_project` validates that the budget is positive and the deadline is in the future.
4. An instance of `Project` is saved in `db.sqlite3` with `status = 'Open'` and linked to `request.user`.

### 4.2 Proposal Submission (Student)
1. A student accesses `/projects/` and filters available opportunities.
2. The student clicks on `/projects/<id>/` to view detailed requirements.
3. The student submits `ProposalForm` with proposed rate, estimated days, and pitch.
4. `views.submit_proposal` verifies:
   - The user possesses the `Student` role.
   - The project is `Open`.
   - No prior proposal from this student exists for this project.
5. A `Proposal` record is created with `status = 'Pending'`.

### 4.3 Proposal Acceptance & Rejection (Client)
1. The client opens `/projects/<id>/proposals/` to review student bids.
2. Clicking **Accept**:
   - The selected proposal status is updated to `Accepted`.
   - The project status is transitioned to `Assigned`.
   - All other proposals associated with this project that remain in `Pending` are set to `Rejected`.

---

## 5. Security & Validation Controls

| Threat / Risk | Django Mitigation Implemented |
|---|---|
| **Plain-text Credentials** | PBKDF2 with SHA-256 password hashing via `User.set_password()`. |
| **Cross-Site Request Forgery (CSRF)** | `CsrfViewMiddleware` and `{% csrf_token %}` on all forms. |
| **SQL Injection** | Parameterized queries handled by Django ORM (`filter()`, `get()`). |
| **Cross-Site Scripting (XSS)** | Built-in HTML escaping in Django Template Language (`{{ variable }}`). |
| **Privilege Escalation** | Custom role decorators (`@student_required`, `@client_required`, `@admin_required`). |
| **Duplicate Bidding** | `unique_together = ('project', 'student')` constraint in the database. |

---

## 6. Testing & Quality Assurance Summary

Automated testing was conducted using Django's built-in `TestCase` harness in `marketplace/tests.py`.

```text
Found 17 test(s).
Creating test database for alias 'default'...
.................
----------------------------------------------------------------------
Ran 17 tests in 49.262s

OK
Destroying test database for alias 'default'...
System check identified no issues (0 silenced).
```

### Verified Test Cases:
1. `test_student_registration`: Registers student user and creates profile.
2. `test_client_registration`: Registers client user and creates profile.
3. `test_login_and_logout`: Confirms session creation and teardown.
4. `test_student_dashboard_access`: Verifies authorized dashboard access.
5. `test_profile_editing`: Confirms user and profile record mutation.
6. `test_project_listing_and_search`: Tests keyword search and category filtering.
7. `test_proposal_submission_and_duplicate_prevention`: Ensures duplicate submission rejection.
8. `test_my_proposals_page`: Validates display of student bids and status tags.
9. `test_client_post_project_create`: Validates project record insertion.
10. `test_client_edit_project_update`: Validates client project editing.
11. `test_client_delete_project_delete`: Validates project deletion.
12. `test_client_accept_and_reject_proposal`: Tests automatic status transitions.
13. `test_student_cannot_access_client_pages`: Enforces role authorization boundaries.
14. `test_client_cannot_access_student_pages`: Enforces role authorization boundaries.
15. `test_client_cannot_edit_other_clients_project`: Prevents cross-tenant project modification.
16. `test_unauthenticated_cannot_access_protected_pages`: Enforces login redirection.
17. `test_admin_dashboard_access`: Restricts administrative dashboard to staff members.

---

## 7. Future Enhancements

1. **Payment Gateway Integration:** Incorporating Razorpay or Stripe test modes for project escrow.
2. **Real-time Messaging:** Integrating Django Channels and WebSockets for direct student-client messaging.
3. **Rating & Reviews:** Allowing clients to rate students after project completion and write testimonials.
4. **Portfolio File Uploads:** Adding Amazon S3 / Cloudinary storage for student attachments and deliverables.

