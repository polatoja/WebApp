from django.test import TestCase
from django.urls import reverse
from early_tasks.models import Task, User, UserProfile

class ManageTasksTest(TestCase):
    def setUp(self):
        self.manager = User.objects.create_user(username='manager', password='managerpass')
        self.user_profile = UserProfile.objects.create(user=self.manager, role='manager')
        self.client.login(username='manager', password='managerpass')
        self.task = Task.objects.create(name='Task 1', status='pending', level='medium', created_by=self.manager)

    def test_manage_tasks_page(self):
        response = self.client.get(reverse('manage_tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/manage_tasks.html')

    def test_add_task_with_ajax(self):
        response = self.client.post(reverse('manage_task_action', args=[self.task.id, 'add']),
                                    {'name': 'New Task', 'description': 'test','status': 'pending', 'level': 'easy'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Task.objects.filter(name='Task 1').exists())

    def test_delete_task_with_ajax(self):
        response = self.client.post(reverse('manage_task_action', args=[self.task.id, 'delete']),
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())