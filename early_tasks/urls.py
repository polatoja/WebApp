from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    # Admin panel URL
    path('admin/', admin.site.urls),  # Add this line to include the Django admin panel

    # Authentication and Main Pages
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('accounts/login/', views.custom_login, name='a_login'),
    path('logout/', views.logout, name='logout'),
    path('', views.home, name='home'),  # Home page

    # Task-related Views
    path('view_tasks/', views.view_tasks, name='view_tasks'),   # For normal users to view tasks

    path('completed_tasks/', views.completed_tasks, name='completed_tasks'),   # For normal users to view tasks
    path('completed_tasks/<int:task_id>/<str:action>/', views.completed_tasks, name='completed_tasks'),   # For normal users to view tasks

    path('manage_tasks/', views.manage_tasks, name='manage_tasks'),  # For viewing/adding tasks
    path('manage_tasks/<int:task_id>/<str:action>/', views.manage_tasks, name='manage_task_action'), # For editing/deleting tasks
    path('view_tasks/<int:task_id>/<str:action>/', views.view_tasks, name='view_task_action'),  

    # Changing password
    path('password_reset/', views.reset_password_request, name='password_reset_request'),
    path('password_reset_confirm/<uid>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    #path('password_reset/', auth_views.PasswordResetView.as_view(template_name='tasks/password_reset.html'), name='password_reset'),
]