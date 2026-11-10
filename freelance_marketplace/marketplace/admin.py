from django.contrib import admin
from .models import Profile, Project, Proposal


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'education', 'skills')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'skills', 'education')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'category', 'budget', 'deadline', 'status', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'description', 'client__username')
    date_hierarchy = 'created_at'


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ('project', 'student', 'proposed_amount', 'estimated_days', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('project__title', 'student__username', 'description')
    date_hierarchy = 'created_at'
