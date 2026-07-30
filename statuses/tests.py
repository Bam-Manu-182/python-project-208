from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from statuses.models import Status

# Create your tests here.

User = get_user_model()


class StatusCRUDTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='password123'
        )
        self.status = Status.objects.create(name='Nuevo')

    def test_status_list_access(self):
        response = self.client.get(reverse('status_list'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('status_list'))
        self.assertEqual(response.status_code, 200)

    def test_status_create(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(
            reverse('status_create'),
            {'name': 'En progreso'}
        )
        self.assertRedirects(response, reverse('status_list'))
        self.assertTrue(Status.objects.filter(name='En progreso').exists())

    def test_status_update(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(
            reverse('status_update', args=[self.status.id]),
            {'name': 'Modificado'}
        )
        self.assertRedirects(response, reverse('status_list'))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Modificado')

    def test_status_delete(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(
            reverse('status_delete', args=[self.status.id])
        )
        self.assertRedirects(response, reverse('status_list'))
        self.assertFalse(Status.objects.filter(id=self.status.id).exists())
