import smtplib
import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, TemplateView, ListView

from mailing.models import Mailing, Client
from users.form import UsersRegisterForm
from users.models import Users


@login_required
def profile(request):
    return render(request, 'users/profile.html')


@method_decorator(cache_page(60 * 5), name='dispatch')
class HomeView(TemplateView):
    template_name = 'users/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_staff:
            context['total_mailings'] = Mailing.objects.all().count()
            context['active_mailings'] = Mailing.objects.filter(status='running').count()
            context['unique_clients'] = len(Client.objects.all().values_list('email', flat=True).distinct())
            context['mailings'] = Mailing.objects.all()
        else:
            context['user_mailings_count'] = Mailing.objects.filter(user=self.request.user).count()
            context['user_active_mailings_count'] = Mailing.objects.filter(status='running',
                                                                           user=self.request.user).count()
            context['user_unique_clients_count'] = len(
                Client.objects.filter(user=self.request.user).values_list('email', flat=True).distinct())
        return context


class UserRegisterView(CreateView):
    model = Users
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    form_class = UsersRegisterForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.email_verify = False
        user.token = str(uuid.uuid4())
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
    success_url = reverse_lazy('home')
    form_class = AuthenticationForm

    def form_invalid(self, form):
        messages.error(self.request, 'Неверный логин или пароль. Пожалуйста, попробуйте снова.')
        return super().form_invalid(form)


class VerifyEmailView(View):
    """Представление для подтверждения почты"""
    def get(self, request, token):
        user = Users.objects.filter(token=token).first()
        if user:
            user.email_verify = True
            user.token = None
            user.save()
            messages.success(request, 'Ваш email успешно подтвержден! Теперь вы можете войти.')
        else:
            messages.error(request, 'Неверный или просроченный токен подтверждения.')
        return redirect(reverse('users:login'))


class UserLogoutView(LogoutView):
    """Представление для выхода пользователя"""
    next_page = reverse_lazy('home')


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Users
    template_name = 'users/user_list.html'
    context_object_name = 'users'

    def test_func(self):
        return self.request.user.is_staff


class UserBlockView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Представление для блокировки/разблокировки пользователя.
    Доступно только менеджерам.
    """
    def test_func(self):
        return self.request.user.is_staff

    def post(self, request, pk):
        user_to_block = get_object_or_404(Users, pk=pk)
        if user_to_block == request.user or user_to_block.is_superuser:
            messages.error(request, 'Вы не можете заблокировать себя или суперпользователя.')
            return redirect('users:user_list')
        user_to_block.is_active = not user_to_block.is_active
        user_to_block.save()
        if user_to_block.is_active:
            messages.success(request, f'Пользователь {user_to_block.email} разблокирован.')
        else:
            messages.warning(request, f'Пользователь {user_to_block.email} заблокирован.')
        return redirect('users:user_list')
