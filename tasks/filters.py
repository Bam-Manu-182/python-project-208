import django_filters
from django import forms
from .models import Task
from statuses.models import Status
from labels.models import Label
from django.contrib.auth import get_user_model


User = get_user_model()


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label='Estado'
    )

    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label='Ejecutor'
    )

    label = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        field_name='labels',
        label='Etiqueta'
    )

    self_tasks = django_filters.BooleanFilter(
        label='Solo mis tareas',
        method='filter_self_tasks',
        widget=forms.CheckboxInput
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label', 'self_tasks']

    def filter_self_tasks(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(author=self.request.user)
        return queryset
