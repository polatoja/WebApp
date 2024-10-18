from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from early_tasks.models import Task, UserProfile
from early_tasks.utils import role_required
from early_tasks.views import filter_tasks_by_params, get_task_data, gather_task_data
from django.http import JsonResponse, HttpResponseForbidden
from datetime import datetime


class TaskUtilityTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.manager = User.objects.create_user(username='testmanager', password='managerpass')
        
        self.user_profile = UserProfile.objects.create(user=self.user, role='user')
        self.manager_profile = UserProfile.objects.create(user=self.manager, role='manager')
        
        self.task1 = Task.objects.create(name='Task 1', description='task1', status='pending', level='easy', due_date = datetime.now(),assigned_user=self.user, created_by=self.manager)
        self.task2 = Task.objects.create(name='Task 2', description='task2', status='completed', level='hard', due_date = datetime.now(), assigned_user=self.user, created_by=self.manager)
        self.task3 = Task.objects.create(name='Task 3', description='task3', status='in-progress', level='medium', due_date = datetime.now(), assigned_user=self.user, created_by=self.manager)

        self.factory = RequestFactory()

    def test_role_required_decorator_user_role(self):

        @role_required(allowed_roles=['user'])
        def dummy_view(request):
            return JsonResponse({'message': 'Success'}, status=200)

        request = self.factory.get('/')
        request.user = self.user

        response = dummy_view(request)
        self.assertEqual(response.status_code, 200)

    def test_role_required_decorator_manager_role(self):

        @role_required(allowed_roles=['manager'])
        def dummy_view(request):
            return JsonResponse({'message': 'Success'}, status=200)

        request = self.factory.get('/')
        request.user = self.manager

        response = dummy_view(request)
        self.assertEqual(response.status_code, 200)

    def test_role_required_forbidden(self):

        @role_required(allowed_roles=['manager'])
        def dummy_view(request):
            return JsonResponse({'message': 'Success'}, status=200)

        request = self.factory.get('/')
        request.user = self.user

        response = dummy_view(request)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content.decode(), "You do not have permission to access this page.")

    def test_filter_tasks_by_params(self):
        request = self.factory.get('/?level[]=easy&status[]=pending')
        request.user = self.user

        filtered_tasks = filter_tasks_by_params(request)
        self.assertEqual(len(filtered_tasks), 1)
        self.assertEqual(filtered_tasks[0], self.task1)

    def test_filter_tasks_by_user_role(self):
        request = self.factory.get('/?level[]=medium&status[]=in-progress')
        request.user = self.user

        filtered_tasks = filter_tasks_by_params(request)
        self.assertEqual(len(filtered_tasks), 1)
        self.assertEqual(filtered_tasks[0], self.task3)

    def test_get_task_data(self):
        task_data = get_task_data(self.task1)
        expected_data = {
            'id': self.task1.id,
            'name': 'Task 1',
            'description': 'task1',
            'status': 'pending',
            'level': 'easy',
            'due_date': datetime.now().strftime('%d.%m.%Y'),
            'assigned_user': 'testuser',
            'created_by': 'testmanager',
            'rating': None
        }
        self.assertEqual(task_data, expected_data)

    def test_gather_task_data(self):
        tasks = Task.objects.all()
        task_data_list, levels, statuses, ratings = gather_task_data(tasks, ['id', 'name', 'status', 'level'])

        self.assertEqual(len(task_data_list), 3)
        self.assertIn('id', task_data_list[0])
        self.assertEqual(levels, ['easy', 'hard', 'medium'])
        self.assertEqual(statuses, ['completed', 'in-progress', 'pending'])
        self.assertEqual(ratings, [None])