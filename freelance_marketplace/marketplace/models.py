from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Profile model extending Django's built-in User model.
    Stores user role (Student or Client), skills, bio, and education details.
    """
    ROLE_CHOICES = [
        ('Student', 'Student'),
        ('Client', 'Client'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    skills = models.TextField(blank=True, help_text="Comma-separated list of skills (e.g. Python, Django, HTML, CSS)")
    bio = models.TextField(blank=True, help_text="Short biography about yourself or your company")
    education = models.CharField(max_length=200, blank=True, help_text="College/University or degree")

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Project(models.Model):
    """
    Project model representing freelance tasks posted by Clients.
    Students can browse open projects and submit proposals.
    """
    CATEGORY_CHOICES = [
        ('Web Development', 'Web Development'),
        ('Graphic Design', 'Graphic Design'),
        ('Content Writing', 'Content Writing'),
        ('Video Editing', 'Video Editing'),
        ('UI/UX Design', 'UI/UX Design'),
        ('Data Entry', 'Data Entry'),
        ('Programming', 'Programming'),
    ]

    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Assigned', 'Assigned'),
        ('Completed', 'Completed'),
        ('Closed', 'Closed'),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def proposal_count(self):
        return self.proposals.count()


class Proposal(models.Model):
    """
    Proposal model submitted by Students for a specific Project.
    Clients can view proposals and choose to accept or reject them.
    """
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='proposals')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proposals')
    description = models.TextField(help_text="Explain why you are the best fit for this project")
    proposed_amount = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_days = models.PositiveIntegerField(help_text="Estimated time in days to complete the project")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('project', 'student')

    def __str__(self):
        return f"Proposal by {self.student.username} for {self.project.title}"
