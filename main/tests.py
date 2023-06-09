from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import quizCategory, quizQuestions, userSubmittedAnswers

class ViewsTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()

    def test_home_view(self):
        # Test the home view
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_register_view(self):
        # Test the register view with valid form data
        form_data = {
            'username': 'newuser',
            'password': 'newpassword',
            # Include other required form fields
        }
        response = self.client.post(reverse('register'), form_data)
        self.assertEqual(response.status_code, 200)  # Assuming successful form submission
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertContains(response, "Data has been submitted Successfully!")

    # Add more test methods for other views...

    def test_password_reset_request_view(self):
        # Test the password_reset_request view with a valid email address
        form_data = {
            'email': self.user.email,
        }
        response = self.client.post(reverse('password_reset_request'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password_reset_done.html')

    def test_password_reset_request_view_invalid_email(self):
        # Test the password_reset_request view with an invalid email address
        form_data = {
            'email': 'invalid@example.com',
        }
        response = self.client.post(reverse('password_reset_request'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password_reset.html')
        self.assertContains(response, "Invalid email address")

    # Add more test methods for other views...