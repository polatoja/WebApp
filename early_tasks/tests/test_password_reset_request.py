from django.test import TestCase
from django.urls import reverse
from early_tasks.models import User, UserProfile
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

class PasswordResetTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.user_profile = UserProfile.objects.create(user=self.user, role='user')
    
    def test_password_reset_request_view_renders_template(self):
        response = self.client.get(reverse('password_reset_request'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/password_reset.html')

    def test_password_reset_request_ajax_post_success(self):
        response = self.client.post(reverse('password_reset_request'), 
                                    {'email': 'test@example.com'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True})

    def test_password_reset_request_ajax_post_user_not_found(self):
        response = self.client.post(reverse('password_reset_request'),
                                    {'email': 'nonexistent@example.com'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'error': 'User with this email does not exist.'})