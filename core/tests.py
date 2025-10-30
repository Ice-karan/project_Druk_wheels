from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class CoreViewsTestCase(TestCase):
    """Basic tests for core app views"""
    
    def setUp(self):
        """Set up test client and create test user"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_index_page_loads(self):
        """Test that the index page loads successfully"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_user_can_login(self):
        """Test that a user can login"""
        login_successful = self.client.login(
            username='testuser',
            password='testpass123'
        )
        self.assertTrue(login_successful)
    
    def test_unauthenticated_user_redirect(self):
        """Test that unauthenticated users are redirected appropriately"""
        # Adjust this URL based on your actual protected views
        response = self.client.get('/dashboard/')
        # Should redirect to login or return 302
        self.assertIn(response.status_code, [302, 301, 403])


class UserModelTestCase(TestCase):
    """Basic tests for User model"""
    
    def test_user_creation(self):
        """Test creating a new user"""
        user = User.objects.create_user(
            username='newuser',
            email='newuser@example.com',
            password='newpass123'
        )
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.email, 'newuser@example.com')
        self.assertTrue(user.check_password('newpass123'))