from django.http import HttpResponseForbidden
from .models import UserProfile
from .models import Task

# in views so we can define who is allowed where
def role_required(allowed_roles):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                profile = UserProfile.objects.get(user=request.user)
                if profile.role in allowed_roles:
                    return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("You do not have permission to access this page.")
        return wrapper
    return decorator

def filter_tasks_by_params(request, extra_filters=None):

    # level filter
    selected_levels = request.GET.getlist('level[]')
    if not selected_levels:
        selected_levels = ['easy', 'medium', 'hard']

    tasks = Task.objects.filter(level__in=selected_levels)

    # status filter
    selected_statuses = request.GET.getlist('status[]')
    if selected_statuses:
        tasks = tasks.filter(status__in=selected_statuses)

    # role filter
    if request.user.userprofile.role == 'user':
        tasks = tasks.filter(assigned_user=request.user)
    elif request.user.userprofile.role == 'manager':
        tasks = tasks.filter(created_by=request.user)
    
    # rating filter
    selected_ratings = request.GET.getlist('rating[]')
    if selected_ratings:
        # ratings can be 1 to 5 or None
        # setting null for none
        null_selected = 'null' in selected_ratings
        int_ratings = [int(r) for r in selected_ratings if r != 'null']

        # with rating
        tasks_with_ratings = tasks.filter(rating__in=int_ratings) if int_ratings else Task.objects.none()

        # without rating
        tasks_with_null_ratings = tasks.filter(rating__isnull=True) if null_selected else Task.objects.none()

        # together
        tasks = tasks_with_ratings | tasks_with_null_ratings

    if extra_filters:
        tasks = tasks.filter(**extra_filters)

    return tasks

def get_task_data(task, fields = None):
   
    if fields is None:
        fields = ['id', 'name', 'description', 'status', 'level', 'due_date', 'assigned_user', 'created_by', 'rating']

    task_data = {}

    for field in fields:
        if field == 'assigned_user':
            task_data[field] = task.assigned_user.username if task.assigned_user else 'None'
        elif field == 'created_by':
            task_data[field] = task.created_by.username if task.created_by else 'Unknown'
        elif field == 'due_date':
            task_data[field] = task.due_date.strftime('%d.%m.%Y') if task.due_date else 'N/A'
        else:
            task_data[field] = getattr(task, field, None)  # field not existing -> None

    return task_data

def gather_task_data(tasks, fields):
    """Utility to gather task data and unique levels and statuses."""
    tasks_list = []
    levels, statuses, ratings = set(), set(), set()
    
    for task in tasks:
        tasks_list.append(get_task_data(task, fields))
        levels.add(task.level)
        statuses.add(task.status)
        if hasattr(task, 'rating'):
            ratings.add(task.rating)
    
    return tasks_list, sorted(levels), sorted(statuses), sorted(ratings, key=lambda x: (x is not None, x))