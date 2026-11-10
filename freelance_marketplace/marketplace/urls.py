from django.urls import path
from . import views

urlpatterns = [
    # Public URLs
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('projects/', views.projects_list, name='projects'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),

    # Student URLs
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('profile/', views.student_profile, name='student_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.student_profile, name='user_profile'),
    path('projects/<int:project_id>/apply/', views.submit_proposal, name='submit_proposal'),
    path('my-proposals/', views.my_proposals, name='my_proposals'),

    # Client URLs (CRUD)
    path('dashboard/client/', views.client_dashboard, name='client_dashboard'),
    path('projects/post/', views.post_project, name='post_project'),
    path('my-projects/', views.my_projects, name='my_projects'),
    path('projects/<int:project_id>/edit/', views.edit_project, name='edit_project'),
    path('projects/<int:project_id>/delete/', views.delete_project, name='delete_project'),
    path('projects/<int:project_id>/proposals/', views.view_proposals, name='view_proposals'),
    path('proposals/<int:proposal_id>/accept/', views.accept_proposal, name='accept_proposal'),
    path('proposals/<int:proposal_id>/reject/', views.reject_proposal, name='reject_proposal'),

    # Admin Dashboard URL
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
