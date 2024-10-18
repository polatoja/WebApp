from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    # BIG BOSS aka admin; Django Admin Panel
    path('admin/', admin.site.urls),

    # main and auth pages
    path('', views.home, name='home'),  # home page
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('accounts/login/', views.custom_login, name='a_login'),
    path('logout/', views.logout, name='logout'),

    # tasks pages
    path('view_tasks/', views.view_tasks, name='view_tasks'),
    path('view_tasks/<int:task_id>/<str:action>/', views.view_tasks, name='view_task_action'), 

    path('completed_tasks/', views.completed_tasks, name='completed_tasks'),
    path('completed_tasks/<int:task_id>/<str:action>/', views.completed_tasks, name='completed_tasks'),

    path('manage_tasks/', views.manage_tasks, name='manage_tasks'), # add
    path('manage_tasks/<int:task_id>/<str:action>/', views.manage_tasks, name='manage_task_action'), # edit/delete

    # password pages
    path('password_reset/', views.reset_password_request, name='password_reset_request'),
    path('password_reset_confirm/<uid>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    
]