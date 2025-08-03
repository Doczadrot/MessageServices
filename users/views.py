from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

# Импортируем модели из нашего приложения mailing, чтобы использовать их для статистики
from mailing.models import Mailing, Client

from users.form import UsersRegisterForm
from users.models import Users

@login_required
def profile(request):
    return render(request, 'users/profile.html')

# Создаем наш HomeView с логикой для сбора статистики
class HomeView(TemplateView):
    """Отображает статистику на главной странице"""
    template_name = 'users/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_mailings'] = Mailing.objects.all().count()
        context['active_mailings'] = Mailing.objects.filter(status='running').count()

        if self.request.user.is_authenticated:

            unique_emails = Client.objects.filter(user=self.request.user).values_list('email', flat=True).distinct()
            context['unique_recipients'] = len(unique_emails)
        else:
            context['unique_recipients'] = 0

        return context

# Create your views here.
class UserRegisterView(CreateView):
    model = Users
    template_name = 'users/register.html'
    success_url = '/'
    form_class = UsersRegisterForm

class UserLoginView(LoginView):
    model = Users
    template_name = 'users/login.html'
    success_url = reverse_lazy('users:home')
    form_class = AuthenticationForm
