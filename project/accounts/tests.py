from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import SignUpForm, LoginForm


class AccountsFormsTests(TestCase):
    def test_signup_form_valid_data(self):
        form = SignUpForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'complex_password123',
            'password2': 'complex_password123',
        })
        self.assertTrue(form.is_valid())

    def test_signup_form_invalid_data(self):
        # Test with mismatched passwords
        form = SignUpForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'complex_password123',
            'password2': 'different_password',
        })
        self.assertFalse(form.is_valid())

    def test_login_form_valid_data(self):
        # Create a user first
        User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='complex_password123'
        )
        
        form = LoginForm(data={
            'username': 'testuser',
            'password': 'complex_password123',
        })
        self.assertTrue(form.is_valid())

    def test_login_form_invalid_data(self):
        # Create a user first
        User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='complex_password123'
        )
        
        form = LoginForm(data={
            'username': 'testuser',
            'password': 'wrong_password',
        })
        self.assertFalse(form.is_valid())


class AccountsViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('accounts:signup')
        self.login_url = reverse('accounts:login')
        self.logout_url = reverse('accounts:logout')
        
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='complex_password123'
        )

    def test_signup_view_GET(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')
        self.assertIsInstance(response.context['form'], SignUpForm)

    def test_signup_view_POST_valid(self):
        response = self.client.post(self.signup_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complex_password123',
            'password2': 'complex_password123',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful signup
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_signup_view_POST_invalid(self):
        response = self.client.post(self.signup_url, {
            'username': 'newuser',
            'email': 'invalid-email',
            'password1': 'password',
            'password2': 'different',
        })
        self.assertEqual(response.status_code, 200)  # Form is redisplayed
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_login_view_GET(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertIsInstance(response.context['form'], LoginForm)

    def test_login_view_POST_valid(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'complex_password123',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_view_POST_invalid(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrong_password',
        })
        self.assertEqual(response.status_code, 200)  # Form is redisplayed
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout_view(self):
        # Login first
        self.client.login(username='testuser', password='complex_password123')
        self.assertTrue(self.client.session.get('_auth_user_id'))
        
        # Then logout
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)  # Redirect after logout
        self.assertFalse(self.client.session.get('_auth_user_id'))
