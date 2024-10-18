from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from .models import Task
from .forms import TaskForm
from django.http import JsonResponse

def add_task(request):
    form = TaskForm(request.POST)
    if form.is_valid():
        task = form.save()
        task.created_by = request.user
        task.save()
        task_data = model_to_dict(task)
        task_data['assigned_user'] = task.assigned_user.username if task.assigned_user else 'None'
        task_data['created_by'] = task.created_by.username if task.created_by else 'None'
        task_data['due_date'] = task.due_date.strftime('%d.%m.%Y') if task.due_date else 'N/A'
        return JsonResponse({'task': task_data}, status=201)
    else:
        return JsonResponse({'errors': form.errors}, status=400)


def delete_task(task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return JsonResponse({'status': 'deleted', 'task_id': task_id}, status=200)

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    form = TaskForm(request.POST, instance=task) # pre-fill
    if form.is_valid():
        task = form.save()
        task_data = model_to_dict(task)
        task_data['assigned_user'] = task.assigned_user.username if task.assigned_user else 'None'
        task_data['created_by'] = task.created_by.username if task.created_by else 'None'
        task_data['due_date'] = task.due_date.strftime('%d.%m.%Y') if task.due_date else 'N/A'
        return JsonResponse({'task': task_data}, status=200)
    else:
        return JsonResponse({'errors': form.errors}, status=400)
