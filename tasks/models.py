from django.db import models
from django.contrib.auth import get_user_model
from statuses.models import Status

# Create your models here.

User = get_user_model()


class Task(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre')
    description = models.TextField(blank=True, verbose_name='Descripción')
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name='Estado'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='created_tasks',
        verbose_name='Autor'
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='executor_tasks',
        null=True,
        blank=True,
        verbose_name='Ejecutor'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    def __str__(self):
        return self.name
