from django.test import TestCase
from django.urls import reverse
from early_tasks.models import Task, User, UserProfile
from django.forms.models import model_to_dict

class TaskManagementTest(TestCase):

    def setUp(self):
        # Create a user and log them in
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user_profile = UserProfile.objects.create(user=self.user, role='manager')  # Assuming you have UserProfile
        self.client.login(username='testuser', password='testpass')

        # Create a task
        self.task = Task.objects.create(
            name='Test Task',
            status='pending',
            level='medium',
            created_by=self.user
        )

    def test_add_task(self):
        # Test adding a task via AJAX
        response = self.client.post(
            reverse('manage_task_action', args=[0, 'add']),  # Adjust the URL pattern accordingly
            {'name': 'New Task', 'status': 'pending', 'level': 'medium'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Task.objects.filter(name='New Task').exists())
        new_task = Task.objects.get(name='New Task')
        task_data = model_to_dict(new_task)
        self.assertEqual(task_data['name'], 'New Task')

    def test_delete_task(self):
        # Test deleting a task
        response = self.client.post(
            reverse('manage_task_action', args=[self.task.id, 'delete']),  # Adjust the URL pattern accordingly
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_edit_task(self):
        # Test editing a task
        response = self.client.post(
            reverse('manage_task_action', args=[self.task.id, 'edit']),  # Adjust the URL pattern accordingly
            {'name': 'Edited Task', 'status': 'completed', 'level': 'high'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Edited Task')
        self.assertEqual(self.task.status, 'completed')
        self.assertEqual(self.task.level, 'high')

