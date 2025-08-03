from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView, TemplateView

# Импортируем все формы и модели, с которыми мы работаем
from mailing.forms import MessageForm, ClientForm, MailingForm
from mailing.models import Message, Client, Mailing, Mailjurnal
from mailing.services import send_mailing


# ----- Представления для сообщений -----
class MessageCreateView(LoginRequiredMixin, CreateView):
    """Представление для создания нового сообщения."""
    model = Message
    success_url = reverse_lazy('mailing:message_list')
    form_class = MessageForm

    def form_valid(self, form):
        """Метод для автоматического присвоения владельца сообщению."""
        # Текущий пользователь (self.request.user) становится владельцем сообщения.
        form.instance.user = self.request.user
        return super().form_valid(form)

class MessageListView(LoginRequiredMixin, ListView):
    """Представление для отображения списка сообщений."""
    model = Message
    context_object_name = 'messages'
    template_name = 'mailing/message_list.html'

    def get_queryset(self):
        """Фильтрация сообщений по текущему пользователю."""
        # Показываем только те сообщения, которые создал текущий пользователь.
        return Message.objects.filter(user=self.request.user)

class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """Представление для редактирования сообщения."""
    model = Message
    success_url = reverse_lazy('mailing:message_list')
    form_class = MessageForm

class MessageDetailView(LoginRequiredMixin, DetailView):
    """Представление для отображения деталей сообщения."""
    model = Message
    context_object_name = 'message'

class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """Представление для удаления сообщения."""
    model = Message
    success_url = reverse_lazy('mailing:message_list')
    template_name = 'mailing/message_confirm_delete.html'


# ----- Представления для клиентов -----
class ClientCreateView(LoginRequiredMixin, CreateView):
    """Представление для создания нового клиента."""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        """Метод для автоматического присвоения владельца клиенту."""
        # Текущий пользователь становится владельцем клиента.
        form.instance.user = self.request.user
        return super().form_valid(form)

class ClientListView(LoginRequiredMixin, ListView):
    """Представление для отображения списка клиентов."""
    model = Client
    context_object_name = 'clients'
    template_name = 'mailing/client_list.html'

    def get_queryset(self):
        """Фильтрация клиентов по текущему пользователю."""
        # Показываем только тех клиентов, которые принадлежат текущему пользователю.
        return Client.objects.filter(user=self.request.user)

class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """Представление для редактирования клиента."""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """Представление для удаления клиента."""
    model = Client
    success_url = reverse_lazy('mailing:client_list')
    template_name = 'mailing/client_confirm_delete.html'

class ClientDetailView(LoginRequiredMixin, DetailView):
    """Представление для отображения деталей клиента."""
    model = Client
    context_object_name = 'client'

class MailingCreateView(LoginRequiredMixin, CreateView):
    """Представление для создания новой рассылки."""
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form_kwargs(self):
        """Передаем текущего пользователя в форму."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class MailingListView(LoginRequiredMixin, ListView):
    """Представление для отображения списка рассылок."""
    model = Mailing
    context_object_name = 'mailings'
    template_name = 'mailing/mailing_list.html'

    def get_queryset(self):
        # Эта строка фильтрует рассылки, показывая только те,
        # что принадлежат текущему авторизованному пользователю
        return Mailing.objects.filter(message__user=self.request.user)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """Представление для создания новой рассылки."""
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form_kwargs(self):
        """Передаем текущего пользователя в форму."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class MailingDetailView(LoginRequiredMixin, DetailView):
    """Представление для отображения деталей клиента."""
    model = Mailing
    context_object_name = 'mailing'

class MailingDeleteView(LoginRequiredMixin, DeleteView):
    """Представление для удаления клиента."""
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')
    template_name = 'mailing/mailing_confirm_delete.html'

class MailingSendView(LoginRequiredMixin, View):
    """
    Представление для ручной отправки рассылки.
    """
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk, message__user=self.request.user)
        # Вызываем функцию из нашего сервиса
        send_mailing(mailing)
        messages.success(request, f'Рассылка "{mailing.title}" успешно запущена.')
        return redirect('mailing:mailing_list')


# class HomeView(TemplateView):
#     """Отображает статистику на главной странице"""
#     template_name = 'home.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['total_mailings'] = Mailing.objects.all().count()
#         context['active_mailings'] = Mailing.objects.filter(status='running').count()
#
#         if self.request.user.is_authenticated:
#             context['unique_recipients'] = Client.objects.filter(user=self.request.user).distinct('email').count()
#         else:
#             context['unique_recipients'] = 0
#
#         return context

class MailjurnalListView(LoginRequiredMixin, ListView):
    """Представление для отображения журнала рассылок."""
    model = Mailjurnal
    context_object_name = 'journal_entries'
    template_name = 'mailing/mailjurnal_list.html'

    def get_queryset(self):
        # Фильтруем журнал, чтобы показывать записи только для рассылок текущего пользователя
        return Mailjurnal.objects.filter(malling__message__user=self.request.user)

class MailingActivateView(LoginRequiredMixin, View):
    """
    Представление для активации рассылки (установка статуса 'running').
    """
    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk, message__user=self.request.user)
        mailing.status = 'running'
        mailing.save()
        messages.success(request, f'Рассылка "{mailing.title}" успешно активирована.')
        return redirect('mailing:mailing_list')

class MailingPauseView(LoginRequiredMixin, View):
    """
    Представление для приостановки рассылки (установка статуса 'paused').
    """
    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk, message__user=self.request.user)
        mailing.status = 'paused'
        mailing.save()
        messages.success(request, f'Рассылка "{mailing.title}" успешно приостановлена.')
        return redirect('mailing:mailing_list')

class MailingDeactivateView(LoginRequiredMixin, View):
    """
    Представление для деактивации рассылки (установка статуса 'completed').
    """
    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk, message__user=self.request.user)
        mailing.status = 'completed'
        mailing.save()
        messages.success(request, f'Рассылка "{mailing.title}" успешно завершена.')
        return redirect('mailing:mailing_list')
