from django import forms
from .models import Task
from django.contrib.auth import get_user_model


User = get_user_model()

class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name() or obj.username


class TaskForm(forms.ModelForm):
    executor = UserChoiceField(
        queryset=User.objects.all(),
        required=False,
        label='Ejecutor'
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
