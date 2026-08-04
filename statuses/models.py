from django.shortcuts import render
from django.db import models

# Create your models here.

class Status(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    def __str__(self):
        return self.name
