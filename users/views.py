from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import UserCreateForm
from django.db.models import ProtectedError
from django.shortcuts import redirect

# Create your views here.

class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('login')
    success_message = 'Usuario registrado con éxito'


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'username']
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('user_list')
    success_message = 'Usuario actualizado con éxito'

    def test_func(self):
        user = self.get_object()
        return self.request.user == user


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')
    success_message = 'El usuario se eliminó con éxito'

    def test_func(self):
        user = self.get_object()
        return self.request.user == user

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                request,
                'No se puede eliminar un usuario porque está en uso'
            )
            return redirect('user_list')


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'
    next_page = reverse_lazy('index')
    success_message = 'Ha iniciado sesión'


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'Ha cerrado sesión')
        return super().dispatch(request, *args, **kwargs)
