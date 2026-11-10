from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Q

from .models import Profile, Project, Proposal
from .forms import RegistrationForm, LoginForm, ProfileEditForm, ProjectForm, ProposalForm


# ==========================================
# HELPER ROLE DECORATORS / CHECKS
# ==========================================

def get_user_role(user):
    """Safely retrieves the role of a user from their Profile."""
    if not user.is_authenticated:
        return None
    try:
        return user.profile.role
    except Profile.DoesNotExist:
        # If user is staff/admin without a Profile
        if user.is_staff or user.is_superuser:
            return 'Admin'
        return None


def student_required(view_func):
    """Decorator to ensure only authenticated users with Student role can access."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in to access this page.")
            return redirect('login')
        if get_user_role(request.user) != 'Student':
            messages.error(request, "Access denied. This page is only accessible to students.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


def client_required(view_func):
    """Decorator to ensure only authenticated users with Client role can access."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in to access this page.")
            return redirect('login')
        if get_user_role(request.user) != 'Client':
            messages.error(request, "Access denied. This page is only accessible to clients.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    """Decorator to ensure only staff members can access the custom admin dashboard."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in with an administrator account.")
            return redirect('login')
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, "Access denied. Administrator privileges required.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


# ==========================================
# PUBLIC VIEWS
# ==========================================

def home(request):
    """
    Public landing page.
    Displays hero section, project categories with counts, how it works,
    and the latest 6 open freelance projects.
    """
    categories = [
        'Web Development', 'Graphic Design', 'Content Writing',
        'Video Editing', 'UI/UX Design', 'Data Entry', 'Programming'
    ]

    # Calculate count of open projects per category
    category_data = []
    for cat in categories:
        count = Project.objects.filter(category=cat, status='Open').count()
        category_data.append({'name': cat, 'count': count})

    # Latest 6 open projects for featured section
    featured_projects = Project.objects.filter(status='Open').select_related('client')[:6]

    # Quick platform numbers
    total_open_projects = Project.objects.filter(status='Open').count()
    total_students = Profile.objects.filter(role='Student').count()
    total_proposals = Proposal.objects.count()

    context = {
        'categories': category_data,
        'featured_projects': featured_projects,
        'total_open_projects': total_open_projects,
        'total_students': total_students,
        'total_proposals': total_proposals,
    }
    return render(request, 'marketplace/home.html', context)


def register_view(request):
    """
    Handles user registration for both Students and Clients.
    Uses Django's built-in User model and creates a linked Profile.
    """
    if request.user.is_authenticated:
        return redirect_dashboard_by_role(request.user)

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']

            # Create User using Django's built-in manager (handles password hashing)
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # Create linked Profile
            Profile.objects.create(
                user=user,
                role=role
            )

            messages.success(request, f"Welcome {username}! Your account was created successfully.")
            # Automatically log in new user
            login(request, user)
            return redirect_dashboard_by_role(user)
    else:
        form = RegistrationForm()

    return render(request, 'marketplace/register.html', {'form': form})


def login_view(request):
    """
    Handles user login using Django's built-in authenticate and login functions.
    Redirects to the appropriate dashboard based on user role.
    """
    if request.user.is_authenticated:
        return redirect_dashboard_by_role(request.user)

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                return redirect_dashboard_by_role(user)
            else:
                messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = LoginForm()

    return render(request, 'marketplace/login.html', {'form': form})


def logout_view(request):
    """
    Logs out the authenticated user and redirects to the home page.
    """
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('home')


def redirect_dashboard_by_role(user):
    """Helper to redirect authenticated users to their corresponding dashboard."""
    if user.is_staff or user.is_superuser:
        return redirect('admin_dashboard')
    try:
        if user.profile.role == 'Student':
            return redirect('student_dashboard')
        elif user.profile.role == 'Client':
            return redirect('client_dashboard')
    except Profile.DoesNotExist:
        pass
    return redirect('home')


def projects_list(request):
    """
    Public listing of all Open freelance projects.
    Includes search by keyword and filtering by category.
    """
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()

    projects = Project.objects.filter(status='Open').select_related('client')

    if query:
        projects = projects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    if category:
        projects = projects.filter(category=category)

    categories = [
        'Web Development', 'Graphic Design', 'Content Writing',
        'Video Editing', 'UI/UX Design', 'Data Entry', 'Programming'
    ]

    context = {
        'projects': projects,
        'query': query,
        'selected_category': category,
        'categories': categories,
        'total_count': projects.count(),
    }
    return render(request, 'marketplace/projects.html', context)


def project_detail(request, project_id):
    """
    Displays full details of a specific project.
    Students can see if they have already applied and apply if open.
    Clients can see options to manage their project.
    """
    project = get_object_or_404(Project.objects.select_related('client'), id=project_id)

    # Check if current logged-in user is a student who already submitted a proposal
    user_proposal = None
    user_is_student = False
    user_is_client_owner = False

    if request.user.is_authenticated:
        role = get_user_role(request.user)
        if role == 'Student':
            user_is_student = True
            user_proposal = Proposal.objects.filter(project=project, student=request.user).first()
        elif project.client == request.user:
            user_is_client_owner = True

    context = {
        'project': project,
        'user_proposal': user_proposal,
        'user_is_student': user_is_student,
        'user_is_client_owner': user_is_client_owner,
    }
    return render(request, 'marketplace/project_detail.html', context)


# ==========================================
# STUDENT VIEWS
# ==========================================

@student_required
def student_dashboard(request):
    """
    Dashboard for students.
    Dynamically calculates:
    - Total proposals submitted
    - Pending proposals
    - Accepted proposals
    - Rejected proposals
    - Recently posted open projects
    """
    student_proposals = Proposal.objects.filter(student=request.user)

    total_proposals = student_proposals.count()
    pending_proposals = student_proposals.filter(status='Pending').count()
    accepted_proposals = student_proposals.filter(status='Accepted').count()
    rejected_proposals = student_proposals.filter(status='Rejected').count()

    recent_proposals = student_proposals.select_related('project')[:5]
    available_projects = Project.objects.filter(status='Open').exclude(proposals__student=request.user).select_related('client')[:5]

    context = {
        'total_proposals': total_proposals,
        'pending_proposals': pending_proposals,
        'accepted_proposals': accepted_proposals,
        'rejected_proposals': rejected_proposals,
        'recent_proposals': recent_proposals,
        'available_projects': available_projects,
    }
    return render(request, 'marketplace/student_dashboard.html', context)


@login_required
def student_profile(request, username=None):
    """
    Displays profile information for a student or client.
    If username is omitted, displays current user's profile.
    """
    if username:
        user_obj = get_object_or_404(User, username=username)
    else:
        user_obj = request.user

    # Ensure profile exists
    profile, created = Profile.objects.get_or_create(user=user_obj, defaults={'role': 'Student'})

    # If student, fetch completed projects count or accepted proposals
    accepted_count = 0
    if profile.role == 'Student':
        accepted_count = Proposal.objects.filter(student=user_obj, status='Accepted').count()

    context = {
        'profile_user': user_obj,
        'profile': profile,
        'accepted_count': accepted_count,
        'is_own_profile': (request.user == user_obj),
    }
    return render(request, 'marketplace/student_profile.html', context)


@login_required
def edit_profile(request):
    """
    Allows user to edit their full name, email, skills, bio, and education.
    Role cannot be modified.
    """
    profile, _ = Profile.objects.get_or_create(user=request.user, defaults={'role': 'Student'})

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=profile)
        if form.is_valid():
            # Update User model fields
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()

            # Save Profile fields (skills, bio, education)
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('student_profile')
    else:
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        form = ProfileEditForm(instance=profile, initial=initial_data)

    return render(request, 'marketplace/edit_profile.html', {'form': form, 'profile': profile})


@student_required
def submit_proposal(request, project_id):
    """
    Allows a student to submit a proposal for an Open project.
    Validates that:
    1. The project exists and is Open.
    2. The student has not already submitted a proposal for this project.
    3. Proposal amount and estimated days are valid.
    """
    project = get_object_or_404(Project, id=project_id)

    # Check project status
    if project.status != 'Open':
        messages.error(request, "This project is no longer accepting proposals.")
        return redirect('project_detail', project_id=project.id)

    # Check if proposal already exists
    existing_proposal = Proposal.objects.filter(project=project, student=request.user).first()
    if existing_proposal:
        messages.warning(request, "You have already submitted a proposal for this project.")
        return redirect('project_detail', project_id=project.id)

    if request.method == 'POST':
        form = ProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.project = project
            proposal.student = request.user
            proposal.status = 'Pending'
            proposal.save()

            messages.success(request, "Your proposal has been submitted successfully!")
            return redirect('my_proposals')
    else:
        form = ProposalForm()

    context = {
        'project': project,
        'form': form,
    }
    return render(request, 'marketplace/submit_proposal.html', context)


@student_required
def my_proposals(request):
    """
    Lists all proposals submitted by the currently logged-in student.
    Shows project details, proposed amount, days, and current status.
    """
    proposals = Proposal.objects.filter(student=request.user).select_related('project', 'project__client')
    return render(request, 'marketplace/my_proposals.html', {'proposals': proposals})


# ==========================================
# CLIENT VIEWS (CRUD for Projects & Proposals)
# ==========================================

@client_required
def client_dashboard(request):
    """
    Dashboard for clients.
    Dynamically displays:
    - Total projects posted
    - Open projects
    - Completed projects
    - Total proposals received
    - Recent projects posted by this client
    """
    client_projects = Project.objects.filter(client=request.user)

    total_projects = client_projects.count()
    open_projects = client_projects.filter(status='Open').count()
    completed_projects = client_projects.filter(status='Completed').count()

    total_proposals_received = Proposal.objects.filter(project__client=request.user).count()
    recent_projects = client_projects[:5]

    context = {
        'total_projects': total_projects,
        'open_projects': open_projects,
        'completed_projects': completed_projects,
        'total_proposals_received': total_proposals_received,
        'recent_projects': recent_projects,
    }
    return render(request, 'marketplace/client_dashboard.html', context)


@client_required
def post_project(request):
    """
    CRUD: CREATE operation.
    Allows a client to post a new freelance project.
    Validates form fields and sets initial status to 'Open'.
    """
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.client = request.user
            project.status = 'Open'
            project.save()

            messages.success(request, f"Project '{project.title}' posted successfully!")
            return redirect('my_projects')
    else:
        form = ProjectForm(initial={'status': 'Open'})

    return render(request, 'marketplace/post_project.html', {'form': form})


@client_required
def my_projects(request):
    """
    CRUD: READ operation.
    Displays all projects posted by the logged-in client.
    """
    projects = Project.objects.filter(client=request.user).annotate(
        proposals_count=Count('proposals')
    )
    return render(request, 'marketplace/my_projects.html', {'projects': projects})


@client_required
def edit_project(request, project_id):
    """
    CRUD: UPDATE operation.
    Allows client to edit their own project.
    Ensures a client cannot edit another client's project.
    """
    project = get_object_or_404(Project, id=project_id, client=request.user)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, f"Project '{project.title}' updated successfully.")
            return redirect('my_projects')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'marketplace/edit_project.html', {'form': form, 'project': project})


@client_required
def delete_project(request, project_id):
    """
    CRUD: DELETE operation.
    Allows client to delete their own project.
    Ensures a client cannot delete another client's project.
    """
    project = get_object_or_404(Project, id=project_id, client=request.user)

    if request.method == 'POST':
        title = project.title
        project.delete()
        messages.success(request, f"Project '{title}' has been deleted.")
        return redirect('my_projects')

    # If accessed via GET, render a simple confirmation or redirect
    return render(request, 'marketplace/my_projects.html', {
        'projects': Project.objects.filter(client=request.user),
        'delete_confirm_project': project
    })


@client_required
def view_proposals(request, project_id):
    """
    Displays all proposals submitted by students for a client's project.
    Allows client to accept or reject proposals.
    """
    project = get_object_or_404(Project, id=project_id, client=request.user)
    proposals = project.proposals.select_related('student', 'student__profile').all()

    context = {
        'project': project,
        'proposals': proposals,
    }
    return render(request, 'marketplace/view_proposals.html', context)


@client_required
def accept_proposal(request, proposal_id):
    """
    Allows client to accept a student's proposal.
    Actions performed:
    1. Validates the client owns the project.
    2. Sets the proposal status to 'Accepted'.
    3. Sets project status to 'Assigned'.
    4. Automatically rejects other pending proposals for this project.
    """
    proposal = get_object_or_404(Proposal.objects.select_related('project'), id=proposal_id)
    project = proposal.project

    if project.client != request.user:
        messages.error(request, "You do not have permission to manage this project.")
        return redirect('my_projects')

    if project.status == 'Assigned' and proposal.status != 'Accepted':
        messages.warning(request, "This project has already been assigned to another proposal.")
        return redirect('view_proposals', project_id=project.id)

    # Accept this proposal
    proposal.status = 'Accepted'
    proposal.save()

    # Update project status to Assigned
    project.status = 'Assigned'
    project.save()

    # Reject other pending proposals for this project
    project.proposals.exclude(id=proposal.id).filter(status='Pending').update(status='Rejected')

    messages.success(request, f"Proposal from {proposal.student.username} has been accepted! Project is now Assigned.")
    return redirect('view_proposals', project_id=project.id)


@client_required
def reject_proposal(request, proposal_id):
    """
    Allows client to reject a student's proposal.
    """
    proposal = get_object_or_404(Proposal.objects.select_related('project'), id=proposal_id)
    project = proposal.project

    if project.client != request.user:
        messages.error(request, "You do not have permission to manage this project.")
        return redirect('my_projects')

    proposal.status = 'Rejected'
    proposal.save()

    # If the project was assigned to this proposal, revert status back to Open
    if project.status == 'Assigned' and not project.proposals.filter(status='Accepted').exists():
        project.status = 'Open'
        project.save()

    messages.info(request, f"Proposal from {proposal.student.username} was rejected.")
    return redirect('view_proposals', project_id=project.id)


# ==========================================
# ADMIN DASHBOARD VIEW
# ==========================================

@admin_required
def admin_dashboard(request):
    """
    Custom admin dashboard displaying high-level platform statistics:
    - Total Students
    - Total Clients
    - Total Projects
    - Total Proposals
    - Latest 5 projects
    """
    total_students = Profile.objects.filter(role='Student').count()
    total_clients = Profile.objects.filter(role='Client').count()
    total_projects = Project.objects.count()
    total_proposals = Proposal.objects.count()

    latest_projects = Project.objects.select_related('client')[:5]
    latest_proposals = Proposal.objects.select_related('student', 'project')[:5]

    context = {
        'total_students': total_students,
        'total_clients': total_clients,
        'total_projects': total_projects,
        'total_proposals': total_proposals,
        'latest_projects': latest_projects,
        'latest_proposals': latest_proposals,
    }
    return render(request, 'marketplace/admin_dashboard.html', context)
