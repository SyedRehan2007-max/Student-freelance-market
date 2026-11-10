from datetime import timedelta
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Profile, Project, Proposal


class MarketplaceTests(TestCase):
    def setUp(self):
        # 1. Create Student User
        self.student_user = User.objects.create_user(
            username='student1',
            email='student1@example.com',
            password='testpassword123',
            first_name='Student',
            last_name='One'
        )
        self.student_profile = Profile.objects.create(
            user=self.student_user,
            role='Student',
            skills='Python, Django',
            education='B.Tech CSE'
        )

        # 2. Create Second Student
        self.student_user2 = User.objects.create_user(
            username='student2',
            email='student2@example.com',
            password='testpassword123',
            first_name='Student',
            last_name='Two'
        )
        self.student_profile2 = Profile.objects.create(
            user=self.student_user2,
            role='Student',
            skills='Graphic Design'
        )

        # 3. Create Client User
        self.client_user = User.objects.create_user(
            username='client1',
            email='client1@example.com',
            password='testpassword123',
            first_name='Client',
            last_name='One'
        )
        self.client_profile = Profile.objects.create(
            user=self.client_user,
            role='Client',
            bio='Software Agency'
        )

        # 4. Create Another Client
        self.other_client_user = User.objects.create_user(
            username='client2',
            email='client2@example.com',
            password='testpassword123',
            first_name='Client',
            last_name='Two'
        )
        self.other_client_profile = Profile.objects.create(
            user=self.other_client_user,
            role='Client'
        )

        # 5. Create Staff / Admin User
        self.admin_user = User.objects.create_superuser(
            username='admin_test',
            email='admin@example.com',
            password='adminpassword123',
            first_name='Admin',
            last_name='User'
        )

        # 6. Create Sample Open Project posted by client1
        self.project = Project.objects.create(
            client=self.client_user,
            title='Build a Django Blog',
            description='A simple blog with markdown support.',
            category='Web Development',
            budget=1500.00,
            deadline=timezone.now().date() + timedelta(days=7),
            status='Open'
        )

        self.client = Client()

    # -------------------------------------------------------------
    # REGISTRATION, LOGIN, LOGOUT
    # -------------------------------------------------------------
    def test_student_registration(self):
        response = self.client.post(reverse('register'), {
            'first_name': 'New',
            'last_name': 'Student',
            'username': 'newstudent',
            'email': 'newstudent@example.com',
            'role': 'Student',
            'password': 'password123',
            'confirm_password': 'password123',
        })
        self.assertEqual(response.status_code, 302)
        new_user = User.objects.get(username='newstudent')
        self.assertEqual(new_user.profile.role, 'Student')

    def test_client_registration(self):
        response = self.client.post(reverse('register'), {
            'first_name': 'New',
            'last_name': 'Client',
            'username': 'newclient',
            'email': 'newclient@example.com',
            'role': 'Client',
            'password': 'password123',
            'confirm_password': 'password123',
        })
        self.assertEqual(response.status_code, 302)
        new_user = User.objects.get(username='newclient')
        self.assertEqual(new_user.profile.role, 'Client')

    def test_login_and_logout(self):
        login_res = self.client.post(reverse('login'), {
            'username': 'student1',
            'password': 'testpassword123'
        })
        self.assertEqual(login_res.status_code, 302)

        logout_res = self.client.get(reverse('logout'))
        self.assertEqual(logout_res.status_code, 302)

    # -------------------------------------------------------------
    # STUDENT FUNCTIONALITY
    # -------------------------------------------------------------
    def test_student_dashboard_access(self):
        self.client.login(username='student1', password='testpassword123')
        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome, Student!')

    def test_profile_editing(self):
        self.client.login(username='student1', password='testpassword123')
        response = self.client.post(reverse('edit_profile'), {
            'first_name': 'Student',
            'last_name': 'Updated',
            'email': 'updated@example.com',
            'skills': 'Python, Django, PostgreSQL',
            'bio': 'Updated student bio',
            'education': 'B.Tech IT',
        })
        self.assertEqual(response.status_code, 302)
        self.student_user.refresh_from_db()
        self.assertEqual(self.student_user.last_name, 'Updated')
        self.assertEqual(self.student_user.profile.skills, 'Python, Django, PostgreSQL')

    def test_project_listing_and_search(self):
        response = self.client.get(reverse('projects'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Build a Django Blog')

        search_res = self.client.get(reverse('projects') + '?q=Django')
        self.assertEqual(search_res.status_code, 200)
        self.assertContains(search_res, 'Build a Django Blog')

        non_matching = self.client.get(reverse('projects') + '?q=UnmatchedKeyword')
        self.assertContains(non_matching, 'No Projects Found')

    def test_proposal_submission_and_duplicate_prevention(self):
        self.client.login(username='student1', password='testpassword123')

        # First proposal submission
        res1 = self.client.post(reverse('submit_proposal', kwargs={'project_id': self.project.id}), {
            'proposed_amount': '1400.00',
            'estimated_days': 5,
            'description': 'I have built multiple Django websites and can finish within 5 days.',
        })
        self.assertEqual(res1.status_code, 302)
        self.assertTrue(Proposal.objects.filter(project=self.project, student=self.student_user).exists())

        # Attempt duplicate submission by same student for same project
        res2 = self.client.get(reverse('submit_proposal', kwargs={'project_id': self.project.id}))
        # Redirects with warning because proposal already exists
        self.assertEqual(res2.status_code, 302)

    def test_my_proposals_page(self):
        Proposal.objects.create(
            project=self.project,
            student=self.student_user,
            proposed_amount=1200.00,
            estimated_days=4,
            description='Test proposal pitch',
            status='Pending'
        )
        self.client.login(username='student1', password='testpassword123')
        response = self.client.get(reverse('my_proposals'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test proposal pitch')
        self.assertContains(response, 'Pending')

    # -------------------------------------------------------------
    # CLIENT CRUD OPERATIONS
    # -------------------------------------------------------------
    def test_client_post_project_create(self):
        self.client.login(username='client1', password='testpassword123')
        response = self.client.post(reverse('post_project'), {
            'title': 'Create Portfolio Site',
            'description': 'Clean portfolio with Bootstrap',
            'category': 'Web Development',
            'budget': '2000.00',
            'deadline': (timezone.now().date() + timedelta(days=10)).isoformat(),
            'status': 'Open',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Project.objects.filter(title='Create Portfolio Site', client=self.client_user).exists())

    def test_client_edit_project_update(self):
        self.client.login(username='client1', password='testpassword123')
        response = self.client.post(reverse('edit_project', kwargs={'project_id': self.project.id}), {
            'title': 'Build a Django Blog - Updated',
            'description': 'Updated description',
            'category': 'Web Development',
            'budget': '1800.00',
            'deadline': (timezone.now().date() + timedelta(days=8)).isoformat(),
            'status': 'Open',
        })
        self.assertEqual(response.status_code, 302)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, 'Build a Django Blog - Updated')

    def test_client_delete_project_delete(self):
        self.client.login(username='client1', password='testpassword123')
        project_to_delete = Project.objects.create(
            client=self.client_user,
            title='Delete Me',
            description='Temporary project',
            category='Programming',
            budget=500.00,
            deadline=timezone.now().date() + timedelta(days=5),
            status='Open'
        )
        response = self.client.post(reverse('delete_project', kwargs={'project_id': project_to_delete.id}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Project.objects.filter(id=project_to_delete.id).exists())

    def test_client_accept_and_reject_proposal(self):
        proposal = Proposal.objects.create(
            project=self.project,
            student=self.student_user,
            proposed_amount=1400.00,
            estimated_days=4,
            description='I will deliver quality work.',
            status='Pending'
        )
        proposal2 = Proposal.objects.create(
            project=self.project,
            student=self.student_user2,
            proposed_amount=1500.00,
            estimated_days=6,
            description='Second applicant pitch.',
            status='Pending'
        )

        self.client.login(username='client1', password='testpassword123')
        
        # Accept first proposal
        accept_res = self.client.get(reverse('accept_proposal', kwargs={'proposal_id': proposal.id}))
        self.assertEqual(accept_res.status_code, 302)

        proposal.refresh_from_db()
        proposal2.refresh_from_db()
        self.project.refresh_from_db()

        self.assertEqual(proposal.status, 'Accepted')
        self.assertEqual(self.project.status, 'Assigned')
        # Second proposal automatically rejected
        self.assertEqual(proposal2.status, 'Rejected')

    # -------------------------------------------------------------
    # SECURITY & ROLE ACCESS RESTRICTIONS
    # -------------------------------------------------------------
    def test_student_cannot_access_client_pages(self):
        self.client.login(username='student1', password='testpassword123')
        # Student trying to post project
        response = self.client.get(reverse('post_project'))
        self.assertEqual(response.status_code, 302)
        # Student trying to access client dashboard
        res_dash = self.client.get(reverse('client_dashboard'))
        self.assertEqual(res_dash.status_code, 302)

    def test_client_cannot_access_student_pages(self):
        self.client.login(username='client1', password='testpassword123')
        # Client trying to submit proposal
        response = self.client.get(reverse('submit_proposal', kwargs={'project_id': self.project.id}))
        self.assertEqual(response.status_code, 302)
        # Client trying to access student dashboard
        res_dash = self.client.get(reverse('student_dashboard'))
        self.assertEqual(res_dash.status_code, 302)

    def test_client_cannot_edit_other_clients_project(self):
        self.client.login(username='client2', password='testpassword123')
        # client2 tries to edit client1's project -> 404
        response = self.client.get(reverse('edit_project', kwargs={'project_id': self.project.id}))
        self.assertEqual(response.status_code, 404)

    def test_unauthenticated_cannot_access_protected_pages(self):
        # Protected pages redirect to login
        res1 = self.client.get(reverse('student_dashboard'))
        self.assertEqual(res1.status_code, 302)
        self.assertIn('/login/', res1.url)

        res2 = self.client.get(reverse('client_dashboard'))
        self.assertEqual(res2.status_code, 302)
        self.assertIn('/login/', res2.url)

    # -------------------------------------------------------------
    # ADMIN DASHBOARD
    # -------------------------------------------------------------
    def test_admin_dashboard_access(self):
        # Normal user cannot access
        self.client.login(username='student1', password='testpassword123')
        res_fail = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(res_fail.status_code, 302)

        # Admin user can access
        self.client.login(username='admin_test', password='adminpassword123')
        res_admin = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(res_admin.status_code, 200)
        self.assertContains(res_admin, 'Platform Administration Dashboard')
