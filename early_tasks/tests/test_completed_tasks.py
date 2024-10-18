from django.test import TestCase
from django.urls import reverse
from early_tasks.models import Task,User, UserProfile

class CompletedTasksTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user_profile = UserProfile.objects.create(user=self.user, role='user')
        self.client.login(username='testuser', password='testpass')
        self.task = Task.objects.create(name='Completed Task', status='completed', assigned_user=self.user)

    def test_completed_tasks_page(self):
        response = self.client.get(reverse('completed_tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/completed_tasks.html')

    def test_rate_task_with_ajax(self):
        response = self.client.post(reverse('completed_tasks', args=[self.task.id, 'rate']),
                                    {'rating': '5'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(self.task.rating, 5)

    def test_invalid_rating(self):
        response = self.client.post(reverse('completed_tasks', args=[self.task.id, 'rate']),
                                    {'rating': 'invalid'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)