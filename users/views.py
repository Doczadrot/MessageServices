import smtplib
import uuid

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, TemplateView

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
    success_url = reverse_lazy('users:login')
    form_class = UsersRegisterForm

    def form_valid(self, form):
        user = form.save(commit=False) # не сохраняем в БД
        user.email_verify = False
        user.token = str(uuid.uuid4()) #создаем уникальный токен для ссылки
        user.save()
        verify_link = self.request.build_absolute_uri(reverse('users:verify_email', args=[user.token]))
        try:
            send_mail(
                'Подтверждение почты',
                f'Для подтверждения почты, перейдите по ссылке: {verify_link}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
        except smtplib.SMTPException:
            pass
        return super().form_valid(form)

class UserLoginView(LoginView):
    model = Users
    template_name = 'users/login.html'
    success_url = reverse_lazy('users:home')
    form_class = AuthenticationForm

class VerifyEmailView(View):
    """Представление для подтверждения почты"""
    def get(self, request, token):
        user = Users.objects.filter(token=token).first()
        if user:
            user.email_verify = True
            user.token = None
            user.save()
            # Добавляем сообщение если успешно
        return redirect(reverse('users:login'))

class UserLogoutView(LogoutView):
    """Представление для выхода пользователя"""
    next_page = reverse_lazy('users:home')
