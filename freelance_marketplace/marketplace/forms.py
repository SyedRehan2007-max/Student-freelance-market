from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Profile, Project, Proposal


class RegistrationForm(forms.Form):
    """
    User registration form handling User and Profile creation.
    Allows registering as either a 'Student' or 'Client'.
    """
    ROLE_CHOICES = [
        ('Student', 'Student / Freelancer'),
        ('Client', 'Client (Project Poster)'),
    ]

    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a username'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'})
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password', 'id': 'id_password'}),
        help_text="Minimum 6 characters recommended."
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password', 'id': 'id_confirm_password'})
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("A user with this username already exists.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        if password and len(password) < 6:
            self.add_error('password', "Password must be at least 6 characters long.")

        return cleaned_data


class LoginForm(forms.Form):
    """
    Simple login form for username and password.
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'id': 'id_login_password'})
    )


class ProfileEditForm(forms.ModelForm):
    """
    Form for editing user profile information (skills, bio, education)
    along with basic user fields (first_name, last_name, email).
    Role cannot be changed.
    """
    first_name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )

    class Meta:
        model = Profile
        fields = ['skills', 'bio', 'education']
        widgets = {
            'skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Python, Django, HTML, CSS, Graphic Design'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Brief description of yourself, your background, and your interests'}),
            'education': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., B.Tech Computer Science, 3rd Year'}),
        }


class ProjectForm(forms.ModelForm):
    """
    Form for clients to post or edit a freelance project.
    """
    class Meta:
        model = Project
        fields = ['title', 'description', 'category', 'budget', 'deadline', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Create a College Event Website'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Provide clear details, requirements, and deliverables for the project'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'budget': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter budget in ₹', 'min': '1', 'step': '0.01'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_budget(self):
        budget = self.cleaned_data.get('budget')
        if budget is not None and budget <= 0:
            raise ValidationError("Budget must be greater than zero.")
        return budget

    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')
        if deadline and deadline < timezone.now().date():
            raise ValidationError("Deadline cannot be in the past.")
        return deadline


class ProposalForm(forms.ModelForm):
    """
    Form for students to submit a proposal for an open project.
    """
    class Meta:
        model = Proposal
        fields = ['proposed_amount', 'estimated_days', 'description']
        widgets = {
            'proposed_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Your proposed fee in ₹', 'min': '1', 'step': '0.01'}),
            'estimated_days': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of days to complete', 'min': '1'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Why are you the best fit? Mention relevant skills and previous experience.'}),
        }

    def clean_proposed_amount(self):
        amount = self.cleaned_data.get('proposed_amount')
        if amount is not None and amount <= 0:
            raise ValidationError("Proposed amount must be greater than zero.")
        return amount

    def clean_estimated_days(self):
        days = self.cleaned_data.get('estimated_days')
        if days is not None and days <= 0:
            raise ValidationError("Estimated days must be greater than zero.")
        return days

