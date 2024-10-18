from django.test import TestCase
from django.urls import reverse
from early_tasks.models import User, UserProfile
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

class PasswordResetConfirmTest(TestCase):
    
    def setUp(self):
        # Create a user and user profile for testing
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.user_profile = UserProfile.objects.create(user=self.user, role='user')
        self.uid = urlsafe_base64_encode(force_bytes(self.user_profile.pk))
        self.token = default_token_generator.make_token(self.user)
    
    def test_password_reset_confirm_view_renders_template(self):
        # Test the GET request that renders the password reset confirmation page
        response = self.client.get(reverse('password_reset_confirm', args=[self.uid, self.token]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/password_reset_confirm.html')

    def test_password_reset_confirm_ajax_post_success(self):
        # Test a successful password reset through AJAX POST
        response = self.client.post(reverse('password_reset_confirm', args=[self.uid, self.token]),
                                    {'newPassword': 'newsecurepassword'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True})

        # Ensure the password has been changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newsecurepassword'))

    def test_password_reset_confirm_ajax_post_invalid_token(self):
        # Test with an invalid token
        response = self.client.post(reverse('password_reset_confirm', args=[self.uid, 'invalidtoken']),
                                    {'newPassword': 'newsecurepassword'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'error': 'Invalid token.'})

    def test_password_reset_confirm_ajax_post_invalid_uid(self):
        # Test with an invalid uid
        invalid_uid = urlsafe_base64_encode(force_bytes(9999))  # Non-existent user
        response = self.client.post(reverse('password_reset_confirm', args=[invalid_uid, self.token]),
                                    {'newPassword': 'newsecurepassword'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'error': 'Invalid link.'})