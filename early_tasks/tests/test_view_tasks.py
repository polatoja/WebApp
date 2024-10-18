from django.test import TestCase
from django.urls import reverse
from datetime import datetime
from early_tasks.models import Task,User, UserProfile

class ViewTasksTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user_profile = UserProfile.objects.create(user=self.user, role='user')
        self.client.login(username='testuser', password='testpass')
        Task.objects.create(name='Task 1', status='pending', level='medium', assigned_user=self.user, due_date=datetime.now())

    def test_view_tasks_page_renders_correct_template(self):
        response = self.client.get(reverse('view_tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/view_tasks.html')

    def test_view_tasks_with_ajax(self):
        response = self.client.get(reverse('view_tasks'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        tasks = response.json()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]['name'], 'Task 1')