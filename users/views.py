from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.form import UsersRegisterForm
from users.models import Users


# Create your views here.
class UserRegisterView(CreateView):
    model = Users
    template_name = 'user/register.html'
    success_url = reverse_lazy('users:login')
    form_class = UsersRegisterForm

class UserLoginView(LoginView):
    model = Users
    template_name = 'user/login.html'
    success_url = reverse_lazy('users:home')
    form_class = AuthenticationForm