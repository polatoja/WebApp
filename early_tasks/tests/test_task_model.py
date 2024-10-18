from django.test import TestCase
from django.urls import reverse
from early_tasks.models import Task,User
from datetime import date

class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.manager = User.objects.create_user(username='manageruser', password='testpass')
        self.task = Task.objects.create(
            name="Test Task",
            description="Test task description",
            status="pending",
            level="easy",
            due_date=date.today(),
            assigned_user=self.user,
            created_by=self.manager,
            rating=None
        )

    def test_task_creation(self):
        self.assertEqual(self.task.name, "Test Task")
        self.assertEqual(self.task.description, "Test task description")
        self.assertEqual(self.task.status, "pending")
        self.assertEqual(self.task.level, "easy")
        self.assertEqual(self.task.assigned_user, self.user)
        self.assertEqual(self.task.created_by, self.manager)
        self.assertIsNone(self.task.rating)

    def test_task_str(self):
        self.assertEqual(str(self.task), "Test Task - Pending (Easy)")

    def test_task_status_display(self):
        self.assertEqual(self.task.get_status_display(), "Pending")

    def test_task_level_display(self):
        self.assertEqual(self.task.get_level_display(), "Easy")

    def test_task_with_rating(self):
        self.task.rating = 5
        self.task.save()
        self.assertEqual(self.task.rating, 5)

    def test_task_null_assigned_user(self):
        task_no_assignee = Task.objects.create(
            name="Task without assignee",
            description="Task with no assigned user",
            status="pending",
            level="medium",
            due_date=date.today(),
            created_by=self.manager
        )
        self.assertIsNone(task_no_assignee.assigned_user)