# tasks/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate, login 

from .models import Task, UserProfile
from .forms import TaskForm, UserRegistrationForm, UserLoginForm

from .utils import role_required, filter_tasks_by_params, get_task_data, gather_task_data
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from .task_service import add_task, delete_task, edit_task

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator

def home(request):
    """Home page view."""
    return render(request, 'tasks/home.html')

def register(request):

    if request.user.is_authenticated:
        return redirect('home')  # so you can't enter if you are logged in

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # save form
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('home')  # success -> home page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegistrationForm()

    return render(request, 'tasks/register.html', {'form': form})

def custom_login(request):
    """User login view"""

    if request.user.is_authenticated:
        return redirect('home')  # logged in -> home page; can't enter

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # 'sezamie otworz sie' -> authenticating user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)  # login user
                return redirect('home')  # success -> home page
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = UserLoginForm()

    return render(request, 'tasks/login.html', {'form': form})


def reset_password_request(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest': # checking if it is ajax
        if request.method == 'POST':
            email = request.POST.get('email')

            try:
                user = UserProfile.objects.get(user__email=email) # who has that email?
            except UserProfile.DoesNotExist:
                return JsonResponse({'error': 'User with this email does not exist.'}, status=400)

            # creating link to reset password with uid and token unique for each task
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user.user)
            reset_link = request.build_absolute_uri(f'/password_reset_confirm/{uid}/{token}/')

            print(f'Password reset link: {reset_link}')

            return JsonResponse({'success': True})
    
    return render(request, 'tasks/password_reset.html')


def password_reset_confirm(request, uid, token):
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.method == 'POST':

            new_password = request.POST.get('newPassword')

            try:
                uid = force_str(urlsafe_base64_decode(uid)) # in request it was encoded
                user = UserProfile.objects.get(pk=uid) # getting user so we know whose password we are changing
            except (UserProfile.DoesNotExist, ValueError, TypeError, OverflowError):
                return JsonResponse({'error': 'Invalid link.'}, status=400)

            if default_token_generator.check_token(user.user, token): # checking token
                user.user.set_password(new_password)
                user.user.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'error': 'Invalid token.'}, status=400)

    return render(request, 'tasks/password_reset_confirm.html', {'uid': uid, 'token': token})


def logout(request):
    """User logout view"""
    auth_logout(request)  # bye bye; logout
    return redirect('home')  # success -> home page

@login_required
@role_required(['user', 'manager', 'admin'])
def view_tasks(request, task_id=None, action=None):

    tasks = filter_tasks_by_params(request, extra_filters={'status__in': ['pending', 'in_progress']}) # other oage for completed tasks
    fields = ['id', 'name', 'description', 'level', 'assigned_user', 'created_by', 'status'] # fields i task form
    tasks_list, levels, statuses, _ = gather_task_data(tasks, fields) # filters

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.method == 'POST' and action == 'edit' and task_id: # changing status
            task = get_object_or_404(Task, id=task_id)
            new_status = request.POST.get('status')
            if new_status in ['pending', 'in_progress', 'completed']:
                task.status = new_status
                task.save()
                task_data = get_task_data(task,fields)
                return JsonResponse({'task': task_data}, status=200)
            else:
                return JsonResponse({'error': 'Invalid status value'}, status=400)           
        return JsonResponse(tasks_list, safe=False)

    user_role = request.user.userprofile.role # we display different values for different roles

    return render(request, 'tasks/view_tasks.html', {
        'levels': levels,
        'status': statuses,
        'user_role': user_role
    })


@login_required
@role_required(['user', 'manager', 'admin'])
def completed_tasks(request, task_id=None, action=None):
     
    user_filter = {'user': 'assigned_user__pk', 'manager': 'created_by__pk', 'admin': None}
    role_filter = user_filter.get(request.user.userprofile.role)
    
    extra_filters = {'status__in': ['completed']} # only completed
    if role_filter:
        extra_filters[role_filter] = request.user.id
    tasks = filter_tasks_by_params(request, extra_filters=extra_filters)
    fields = ['id', 'name', 'description', 'level', 'assigned_user', 'created_by', 'rating']
    tasks_list, levels, _, ratings = gather_task_data(tasks, fields)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        if request.method == 'POST' and action == 'rate' and task_id: # rating
            task = get_object_or_404(Task, id=task_id)

            if task.status == 'completed':  # double check if task belongs there
                rating = request.POST.get('rating')
                if rating.isdigit() and 1 <= int(rating) <= 5:
                    task.rating = int(rating)
                    task.save()
                    return JsonResponse({'success': True, 'message': 'Rating submitted!'})
                else:
                    return JsonResponse({'error': 'Invalid rating. Must be between 1 and 5.'}, status=400)
            return JsonResponse({'error': 'Cannot rate incomplete task.'}, status=400)

        # manager/admin can delete completed task
        elif request.method == 'POST' and action == 'delete' and task_id:
            return delete_task(task_id)

        return JsonResponse(tasks_list, safe=False)

    user_role = request.user.userprofile.role
    sorted_ratings = sorted(ratings, key=lambda x: (x is not None, x))
    
    return render(request, 'tasks/completed_tasks.html', {
        'levels': levels,
        'user_role': user_role,
        'ratings': sorted_ratings
    })

@login_required
@role_required(['manager', 'admin'])
def manage_tasks(request, task_id=None, action=None):
   
    tasks = filter_tasks_by_params(request)
    fields = ['id', 'name', 'description', 'level', 'assigned_user', 'created_by', 'status', 'due_date']
    tasks_list, levels, statuses, _ = gather_task_data(tasks, fields) # filters

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        
        if request.method == 'POST' and action == 'add':
            return add_task(request)

        elif request.method == 'POST' and action == 'delete' and task_id:
            return delete_task(task_id)

        elif request.method == 'POST' and action == 'edit' and task_id:
            return edit_task(request, task_id)

        # itr is not available for user
        if request.user.userprofile.role == 'manager':
            tasks = Task.objects.filter(created_by=request.user)
        else: 
            tasks = Task.objects.all() # admin sees all
        
        return JsonResponse(tasks_list, safe=False)

    users = User.objects.filter(userprofile__role='user')
    return render(request, 'tasks/manage_tasks.html', {
        'users': users,
        'levels': levels,
        'status': statuses
    })