from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from item.models import Category, Item
from .forms import CategoryForm

class DashboardTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='admin', password='12345', is_staff=True, is_superuser=True)
        self.category = Category.objects.create(name='TestCategory')
        self.item = Item.objects.create(name='TestItem', category=self.category, created_by=self.user)
        self.client.login(username='admin', password='12345')

    def test_dashboard_index_view(self):
        response = self.client.get(reverse('dashboard:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/index.html')

    def test_add_category_view(self):
        response = self.client.post(reverse('dashboard:add_category'), {'name': 'NewCategory'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Category.objects.filter(name='NewCategory').exists())

    def test_promote_user(self):
        response = self.client.post(reverse('dashboard:promote', args=[self.user.id]))
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_staff)
        self.assertTrue(self.user.is_superuser)
