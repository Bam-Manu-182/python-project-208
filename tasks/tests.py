from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from statuses.models import Status
from tasks.models import Task
from labels.models import Label

# Create your tests here.

TEST_PASSWORD = 'password123' # nosec B105 B106
User = get_user_model()


class TaskTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='juan',
            password=TEST_PASSWORD
        )
        self.user2 = User.objects.create_user(
            username='maria',
            password=TEST_PASSWORD
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
        self.client.login(username='juan', password=TEST_PASSWORD)
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Probar el proyecto')

    def test_create_task(self):
        self.client.login(username='juan', password=TEST_PASSWORD)
        response = self.client.post(reverse('task_create'), {
            'name': 'Nueva Tarea',
            'description': 'Descripción corta',
            'status': self.status.id,
            'executor': self.user2.id
        })
        self.assertEqual(response.status_code, 302)  # Redirige tras crear
        self.assertTrue(Task.objects.filter(name='Nueva Tarea').exists())

    def test_task_detail(self):
        self.client.login(username='juan', password=TEST_PASSWORD)
        response = self.client.get(reverse('task_detail', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Escribir pruebas unitarias')

    def test_update_task(self):
        self.client.login(username='juan', password=TEST_PASSWORD)
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
        self.client.login(username='maria', password=TEST_PASSWORD)
        response = self.client.post(reverse('task_delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(id=self.task.id).exists())

    def test_delete_task_by_author_success(self):
        self.client.login(username='juan', password=TEST_PASSWORD)
        response = self.client.post(reverse('task_delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_delete_status_in_use_fails(self):
        self.client.login(username='juan', password=TEST_PASSWORD)
        response = self.client.post(reverse('status_delete', args=[self.status.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(id=self.status.id).exists())


class TaskFilterTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='juan', password=TEST_PASSWORD)
        self.user2 = User.objects.create_user(username='maria', password=TEST_PASSWORD)

        self.status1 = Status.objects.create(name='Nueva')
        self.status2 = Status.objects.create(name='Completada')

        self.label1 = Label.objects.create(name='Bug')
        self.label2 = Label.objects.create(name='Feature')

        self.task1 = Task.objects.create(
            name='Tarea 1',
            status=self.status1,
            author=self.user1,
            executor=self.user2
        )
        self.task1.labels.add(self.label1)

        self.task2 = Task.objects.create(
            name='Tarea 2',
            status=self.status2,
            author=self.user2,
            executor=self.user1
        )
        self.task2.labels.add(self.label2)

    def test_filter_by_status(self):
        self.client.login(username='juan', password=TEST_PASSWORD)
        response = self.client.get(reverse('task_list'), {'status': self.status1.id})
        self.assertContains(response, 'Tarea 1')
        self.assertNotContains(response, 'Tarea 2')

    def test_filter_by_label(self):
        self.client.login(username='juan', password=TEST_PASSWORD)
        response = self.client.get(reverse('task_list'), {'label': self.label2.id})
        self.assertContains(response, 'Tarea 2')
        self.assertNotContains(response, 'Tarea 1')

    def test_filter_self_tasks(self):
        self.client.login(username='juan', password=TEST_PASSWORD)
        response = self.client.get(reverse('task_list'), {'self_tasks': 'on'})
        self.assertContains(response, 'Tarea 1')
        self.assertNotContains(response, 'Tarea 2')
