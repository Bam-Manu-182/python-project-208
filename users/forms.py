from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms


User = get_user_model()

class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(label='Nombre', max_length=150, required=True)
    last_name = forms.CharField(label='Apellidos', max_length=150, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username')


class UserUpdateForm(UserCreateForm):
    pass
