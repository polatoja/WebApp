from django.test import TestCase
from early_tasks.models import UserProfile, User

class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user_profile = UserProfile.objects.create(user=self.user, role='user')

    def test_user_profile_creation(self):
        self.assertEqual(self.user_profile.user.username, 'testuser')
        self.assertEqual(self.user_profile.role, 'user')

    def test_user_profile_str(self):
        self.assertEqual(str(self.user_profile), 'testuser (User)')

    def test_user_profile_role_display(self):
        self.assertEqual(self.user_profile.get_role_display(), 'User')