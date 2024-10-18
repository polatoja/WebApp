from django.contrib import admin
from .models import UserProfile, Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'level', 'due_date', 'assigned_user')
    search_fields = ('name', 'description')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    search_fields = ('user__username', 'role')
