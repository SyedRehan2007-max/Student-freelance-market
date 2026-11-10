from datetime import timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from marketplace.models import Profile, Project, Proposal


class Command(BaseCommand):
    help = "Populate the database with sample users, projects, and proposals for testing."

    def handle(self, *args, **options):
        self.stdout.write("Seeding sample data for Student Freelance Marketplace...")

        # 1. Create Administrator Account
        admin_user, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@freelance.local",
                "first_name": "System",
                "last_name": "Admin",
                "is_staff": True,
                "is_superuser": True,
            }
        )
        if created:
            admin_user.set_password("admin123")
            admin_user.save()
            Profile.objects.get_or_create(user=admin_user, defaults={"role": "Client", "bio": "Platform Administrator"})
            self.stdout.write(self.style.SUCCESS("Created admin user: admin / admin123"))
        else:
            self.stdout.write("Admin user 'admin' already exists.")

        # 2. Create Sample Clients
        clients_data = [
            {
                "username": "client_techcorp",
                "first_name": "Rohan",
                "last_name": "Mehta",
                "email": "rohan@techcorp.sample",
                "bio": "HR Manager at TechCorp Solutions. Hiring talented students for digital web projects.",
            },
            {
                "username": "client_startup",
                "first_name": "Anita",
                "last_name": "Deshmukh",
                "email": "anita@apexmedia.sample",
                "bio": "Founder of Apex Media Agency. Looking for creative designers and video editors.",
            }
        ]

        clients = {}
        for cdata in clients_data:
            user, u_created = User.objects.get_or_create(
                username=cdata["username"],
                defaults={
                    "first_name": cdata["first_name"],
                    "last_name": cdata["last_name"],
                    "email": cdata["email"],
                }
            )
            if u_created:
                user.set_password("password123")
                user.save()
            profile, _ = Profile.objects.get_or_create(
                user=user,
                defaults={"role": "Client", "bio": cdata["bio"]}
            )
            clients[cdata["username"]] = user

        # 3. Create Sample Students
        students_data = [
            {
                "username": "student_alex",
                "first_name": "Alex",
                "last_name": "Morgan",
                "email": "alex.morgan@college.sample",
                "role": "Student",
                "skills": "Python, Django, HTML5, CSS3, Bootstrap, SQLite",
                "bio": "Passionate 3rd-year CS student aiming to become a full-stack Python web developer.",
                "education": "B.Tech Computer Science, 3rd Year",
            },
            {
                "username": "student_priya",
                "first_name": "Priya",
                "last_name": "Sharma",
                "email": "priya.sharma@design.sample",
                "role": "Student",
                "skills": "Figma, Adobe Photoshop, UI/UX Design, Canva, Logo Design",
                "bio": "Creative design student specializing in brand identities and modern UI mockups.",
                "education": "B.Des Communication Design, 2nd Year",
            },
            {
                "username": "student_rahul",
                "first_name": "Rahul",
                "last_name": "Verma",
                "email": "rahul.verma@college.sample",
                "role": "Student",
                "skills": "Content Writing, SEO, Technical Writing, Copywriting, Blogging",
                "bio": "Freelance writer passionate about technology, coding tutorials, and concise writing.",
                "education": "BA English & Journalism, Final Year",
            }
        ]

        students = {}
        for sdata in students_data:
            user, u_created = User.objects.get_or_create(
                username=sdata["username"],
                defaults={
                    "first_name": sdata["first_name"],
                    "last_name": sdata["last_name"],
                    "email": sdata["email"],
                }
            )
            if u_created:
                user.set_password("password123")
                user.save()
            profile, _ = Profile.objects.get_or_create(
                user=user,
                defaults={
                    "role": sdata["role"],
                    "skills": sdata["skills"],
                    "bio": sdata["bio"],
                    "education": sdata["education"],
                }
            )
            students[sdata["username"]] = user

        # 4. Create Sample Projects
        today = timezone.now().date()
        projects_data = [
            {
                "title": "Create a College Event Website",
                "client": clients["client_techcorp"],
                "category": "Web Development",
                "budget": 2500.00,
                "deadline": today + timedelta(days=14),
                "description": (
                    "We need a responsive, multi-page website for an upcoming college technology fest.\n"
                    "Requirements:\n"
                    "- Event schedule and speaker lineup pages\n"
                    "- Registration form with basic validation\n"
                    "- Mobile-friendly layout using HTML, CSS, and Bootstrap\n"
                    "- Clean, modern design matching our tech theme."
                ),
                "status": "Open",
            },
            {
                "title": "Design a Modern Business Logo",
                "client": clients["client_startup"],
                "category": "Graphic Design",
                "budget": 1200.00,
                "deadline": today + timedelta(days=7),
                "description": (
                    "Looking for a clean, minimalist logo for our new tech marketing agency.\n"
                    "Deliverables:\n"
                    "- High resolution PNG and vector SVG files\n"
                    "- Dark and light background variations\n"
                    "- Color palette and typography guidelines."
                ),
                "status": "Open",
            },
            {
                "title": "Build a Personal Portfolio Website",
                "client": clients["client_techcorp"],
                "category": "Web Development",
                "budget": 3000.00,
                "deadline": today + timedelta(days=10),
                "description": (
                    "Need an elegant personal portfolio site showcasing software engineering projects.\n"
                    "Features:\n"
                    "- About Me section and downloadable resume link\n"
                    "- Interactive project showcase cards\n"
                    "- Contact form with frontend validation."
                ),
                "status": "Assigned",
            },
            {
                "title": "Create 10 Social Media Promotional Posters",
                "client": clients["client_startup"],
                "category": "Graphic Design",
                "budget": 1800.00,
                "deadline": today + timedelta(days=5),
                "description": (
                    "Need 10 vibrant Instagram and LinkedIn square graphics promoting student workshops.\n"
                    "Content briefs and branding assets will be provided.\n"
                    "Must be delivered in 1080x1080 resolution."
                ),
                "status": "Open",
            },
            {
                "title": "Write 5 Technical Blog Posts for Python Beginners",
                "client": clients["client_techcorp"],
                "category": "Content Writing",
                "budget": 2000.00,
                "deadline": today + timedelta(days=12),
                "description": (
                    "Looking for clear, beginner-friendly 800-word articles explaining core Python concepts:\n"
                    "1. Variables and Data Types\n"
                    "2. Python Lists and Dictionaries\n"
                    "3. Functions and Return Statements\n"
                    "4. Introduction to Django MTV Architecture\n"
                    "5. Working with SQLite in Python."
                ),
                "status": "Open",
            },
            {
                "title": "Edit YouTube Tech Tutorial Videos",
                "client": clients["client_startup"],
                "category": "Video Editing",
                "budget": 3500.00,
                "deadline": today + timedelta(days=8),
                "description": (
                    "Need basic editing for 3 coding tutorial screencasts.\n"
                    "Tasks:\n"
                    "- Cut pauses, background noise, and filler words\n"
                    "- Add lower-third text captions for key concepts\n"
                    "- Add intro and outro branding cards."
                ),
                "status": "Open",
            },
        ]

        created_projects = []
        for pdata in projects_data:
            project, _ = Project.objects.get_or_create(
                title=pdata["title"],
                defaults=pdata
            )
            created_projects.append(project)

        # 5. Create Sample Proposals
        # Project 3 (Portfolio website) has an Accepted proposal from Alex
        portfolio_proj = created_projects[2]
        Proposal.objects.get_or_create(
            project=portfolio_proj,
            student=students["student_alex"],
            defaults={
                "description": "I have built several responsive portfolio websites using HTML, Bootstrap, and Django. I can complete this in 5 days.",
                "proposed_amount": 2800.00,
                "estimated_days": 5,
                "status": "Accepted",
            }
        )

        # Project 1 (College Event Website) has proposals from Alex and Rahul
        event_proj = created_projects[0]
        Proposal.objects.get_or_create(
            project=event_proj,
            student=students["student_alex"],
            defaults={
                "description": "I specialize in clean Bootstrap web design and can create an engaging event website with registration.",
                "proposed_amount": 2400.00,
                "estimated_days": 7,
                "status": "Pending",
            }
        )

        # Project 2 (Logo) has a proposal from Priya
        logo_proj = created_projects[1]
        Proposal.objects.get_or_create(
            project=logo_proj,
            student=students["student_priya"],
            defaults={
                "description": "Design student with expertise in Figma and vector graphics. I will deliver 3 distinct concept sketches within 2 days.",
                "proposed_amount": 1200.00,
                "estimated_days": 4,
                "status": "Pending",
            }
        )

        self.stdout.write(self.style.SUCCESS("Successfully seeded sample data!"))
        self.stdout.write(self.style.SUCCESS("Sample Accounts available:"))
        self.stdout.write("  Admin:   username='admin', password='admin123'")
        self.stdout.write("  Client:  username='client_techcorp', password='password123'")
        self.stdout.write("  Client:  username='client_startup', password='password123'")
        self.stdout.write("  Student: username='student_alex', password='password123'")
        self.stdout.write("  Student: username='student_priya', password='password123'")
        self.stdout.write("  Student: username='student_rahul', password='password123'")

