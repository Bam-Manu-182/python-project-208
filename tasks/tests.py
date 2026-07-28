from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from statuses.models import Status
from tasks.models import Task

# Create your tests here.

User = get_user_model()


class TaskTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='juan',
            password='password123'
        )
        self.user2 = User.objects.create_user(
            username='maria',
            password='password123'
        )

        self.status = Status.objects.create(name='En progreso')

        self.task = Task.objects.create(
            name='Probar el proyecto',
            description='Escribir pruebas unitarias',
            status=self.status,
            author=self.user1,
            executor=self.user2
        )

    def test_anonymous_user_redirected(self):
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 302)

    def test_task_list_authenticated(self):
        self.client.login(username='juan', password='password123')
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Probar el proyecto')

    def test_create_task(self):
        self.client.login(username='juan', password='password123')
        response = self.client.post(reverse('task_create'), {
            'name': 'Nueva Tarea',
            'description': 'Descripción corta',
            'status': self.status.id,
            'executor': self.user2.id
        })
        self.assertEqual(response.status_code, 302)  # Redirige tras crear
        self.assertTrue(Task.objects.filter(name='Nueva Tarea').exists())

    def test_task_detail(self):
        self.client.login(username='juan', password='password123')
        response = self.client.get(reverse('task_detail', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Escribir pruebas unitarias')

    def test_update_task(self):
        self.client.login(username='juan', password='password123')
        response = self.client.post(reverse('task_update', args=[self.task.id]), {
            'name': 'Probar el proyecto EDITADO',
            'description': 'Descripción editada',
            'status': self.status.id,
            'executor': self.user2.id
        })
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Probar el proyecto EDITADO')

    def test_delete_task_by_non_author_fails(self):
        self.client.login(username='maria', password='password123')
        response = self.client.post(reverse('task_delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(id=self.task.id).exists())

    def test_delete_task_by_author_success(self):
        self.client.login(username='juan', password='password123')
        response = self.client.post(reverse('task_delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_delete_status_in_use_fails(self):
        self.client.login(username='juan', password='password123')
        response = self.client.post(reverse('status_delete', args=[self.status.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(id=self.status.id).exists())
