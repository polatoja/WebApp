import unittest
from django.test import TestCase
from django.urls import reverse

class HomeViewTest(TestCase):
    def test_home_view_status_code(self):
        """Test that the home page returns a 200 status code."""
        response = self.client.get(reverse('home'))  # Assuming 'home' is the URL name for the home view
        self.assertEqual(response.status_code, 200)

    def test_home_view_template_used(self):
        """Test that the correct template is used for the home page."""
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'tasks/home.html')