from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from labels.models import Label
from statuses.models import Status
from tasks.models import Task

# Create your tests here.

TEST_PASSWORD = 'password123'
User = get_user_model()



class LabelCRUDTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password=TEST_PASSWORD
        )
        self.client.login(username='testuser', password=TEST_PASSWORD)

        self.label = Label.objects.create(name='Urgente')

    def test_label_list_view(self):
        """Verificar que la lista de etiquetas carga correctamente"""
        response = self.client.get(reverse('label_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Urgente')

    def test_label_create(self):
        """Verificar la creación de una etiqueta"""
        response = self.client.post(reverse('label_create'), {
            'name': 'Documentación'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name='Documentación').exists())

    def test_label_update(self):
        """Verificar la edición de una etiqueta"""
        response = self.client.post(
            reverse('label_update', kwargs={'pk': self.label.pk}),
            {'name': 'Urgente Modificado'}
        )
        self.assertEqual(response.status_code, 302)
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Urgente Modificado')

    def test_label_delete_success(self):
        """Verificar que se puede borrar una etiqueta si no está en uso"""
        response = self.client.post(
            reverse('label_delete', kwargs={'pk': self.label.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Label.objects.filter(pk=self.label.pk).exists())

    def test_label_delete_protected(self):
        """Verificar que NO se puede borrar una etiqueta asignada a una tarea"""
        status = Status.objects.create(name='En progreso')
        task = Task.objects.create(
            name='Tarea de prueba',
            status=status,
            author=self.user
        )
        task.labels.add(self.label)

        response = self.client.post(
            reverse('label_delete', kwargs={'pk': self.label.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(pk=self.label.pk).exists())
