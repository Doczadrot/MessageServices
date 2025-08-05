from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView, TemplateView


from mailing.forms import MessageForm, ClientForm, MailingForm
from mailing.models import Message, Client, Mailing, Mailjurnal, MailingReport
from mailing.services import send_mailing



class MessageCreateView(LoginRequiredMixin, CreateView):
    """Представление для создания нового сообщения."""
    model = Message
    success_url = reverse_lazy('mailing:message_list')
    form_class = MessageForm

    def form_valid(self, form):
        """Метод для автоматического присвоения владельца сообщению."""
        # Текущий пользователь (self.request.user) становится владельцем сообщения.
        form.instance.user = self.request.user
        form.instance.owner = self.request.user
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

    def get_queryset(self):
        """Менеджеры могут редактировать любое сообщение, обычные пользователи - только свои."""
        if self.request.user.is_staff:
            return Message.objects.all()

        return Message.objects.filter(owner=self.request.user)

class MessageDetailView(LoginRequiredMixin, DetailView):
    """Представление для отображения деталей сообщения."""
    model = Message
    context_object_name = 'message'

    def get_queryset(self):
        """Менеджеры могут просматривать детали любого сообщения, обычные пользователи - только свои."""
        if self.request.user.is_staff:
            return Message.objects.all()
        # Фильтруем по полю 'owner'
        return Message.objects.filter(owner=self.request.user)

class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """Представление для удаления сообщения."""
    model = Message
    success_url = reverse_lazy('mailing:message_list')
    template_name = 'mailing/message_confirm_delete.html'

    def get_queryset(self):
        """Менеджеры могут удалять любое сообщение, обычные пользователи - только свои."""
        if self.request.user.is_staff:
            return Message.objects.all()
        # Фильтруем по полю 'owner'
        return Message.objects.filter(owner=self.request.user)



class ClientCreateView(LoginRequiredMixin, CreateView):
    """Представление для создания нового клиента."""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        """Метод для автоматического присвоения владельца клиенту."""
        # Используем 'owner' для определения владельца, как в вашей модели
        form.instance.owner = self.request.user
        # Если поле 'user' также должно быть заполнено текущим пользователем:
        form.instance.user = self.request.user
        return super().form_valid(form)

class ClientListView(LoginRequiredMixin, ListView):
    """Представление для отображения списка клиентов."""
    model = Client
    context_object_name = 'clients'
    template_name = 'mailing/client_list.html'

    def get_queryset(self):
        """Фильтрация клиентов по текущему пользователю. Менеджеры видят всех клиентов."""
        if self.request.user.is_staff:
            return Client.objects.all()
        # Фильтруем по полю 'owner'
        return Client.objects.filter(owner=self.request.user)

class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """Представление для редактирования клиента."""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def get_queryset(self):
        """Менеджеры могут редактировать любого клиента, обычные пользователи - только своих."""
        if self.request.user.is_staff:
            return Client.objects.all()
        # Фильтруем по полю 'owner'
        return Client.objects.filter(owner=self.request.user)

class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """Представление для удаления клиента."""
    model = Client
    success_url = reverse_lazy('mailing:client_list')
    template_name = 'mailing/client_confirm_delete.html'

    def get_queryset(self):
        """Менеджеры могут удалять любого клиента, обычные пользователи - только своих."""
        if self.request.user.is_staff:
            return Client.objects.all()
        # Фильтруем по полю 'owner'
        return Client.objects.filter(owner=self.request.user)

class ClientDetailView(LoginRequiredMixin, DetailView):
    """Представление для отображения деталей клиента."""
    model = Client
    context_object_name = 'client'

    def get_queryset(self):
        """Менеджеры могут просматривать детали любого клиента, обычные пользователи - только своих."""
        if self.request.user.is_staff:
            return Client.objects.all()
        # Фильтруем по полю 'owner'
        return Client.objects.filter(owner=self.request.user)

# ----- Представления для рассылок -----
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

    def form_valid(self, form):
        """Метод для автоматического присвоения владельца рассылке."""
        # Используем 'owner' для определения владельца, как в вашей модели
        form.instance.owner = self.request.user
        # Если поле 'user' также должно быть заполнено текущим пользователем:
        form.instance.user = self.request.user
        return super().form_valid(form)

class MailingListView(LoginRequiredMixin, ListView):
    """Представление для отображения списка рассылок."""
    model = Mailing
    context_object_name = 'mailings'
    template_name = 'mailing/mailing_list.html'

    def get_queryset(self):
        """Фильтрует рассылки, отображая только те, которые принадлежат текущему авторизованному пользователю.
        Менеджеры видят все рассылки."""
        if self.request.user.is_staff:
            return Mailing.objects.all()
        # Фильтруем по полю 'owner'
        return Mailing.objects.filter(owner=self.request.user)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """Представление для редактирования рассылки."""
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form_kwargs(self):
        """Передаем текущего пользователя в форму."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        """Менеджеры могут редактировать любую рассылку, обычные пользователи - только свои."""
        if self.request.user.is_staff:
            return Mailing.objects.all()
        # Фильтруем по полю 'owner'
        return Mailing.objects.filter(owner=self.request.user)

class MailingDetailView(LoginRequiredMixin, DetailView):
    """Представление для отображения деталей рассылки."""
    model = Mailing
    context_object_name = 'mailing'

    def get_queryset(self):
        """Менеджеры могут просматривать детали любой рассылки, обычные пользователи - только свои."""
        if self.request.user.is_staff:
            return Mailing.objects.all()
        # Фильтруем по полю 'owner'
        return Mailing.objects.filter(owner=self.request.user)

class MailingDeleteView(LoginRequiredMixin, DeleteView):
    """Представление для удаления рассылки."""
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')
    template_name = 'mailing/mailing_confirm_delete.html'

    def get_queryset(self):
        """Менеджеры могут удалять любую рассылку, обычные пользователи - только свои."""
        if self.request.user.is_staff:
            return Mailing.objects.all()
        # Фильтруем по полю 'owner'
        return Mailing.objects.filter(owner=self.request.user)

class MailingSendView(LoginRequiredMixin, View):
    """Представление для ручной отправки рассылки."""
    def post(self, request, pk):
        # Менеджеры могут отправлять любую рассылку, обычные пользователи - только свои
        if self.request.user.is_staff:
            mailing = get_object_or_404(Mailing, pk=pk)
        else:
            # Используем 'owner' для фильтрации
            mailing = get_object_or_404(Mailing, pk=pk, owner=self.request.user)
        send_mailing(mailing)
        messages.success(request, f'Рассылка "{mailing.title}" успешно запущена.')
        return redirect('mailing:mailing_list')

# Представление для журнала рассылок
class MailjurnalListView(LoginRequiredMixin, ListView):
    """Представление для отображения журнала рассылок."""
    model = Mailjurnal
    context_object_name = 'journal_entries'
    template_name = 'mailing/mailjurnal_list.html'

    def get_queryset(self):
        """Фильтрует журнал, чтобы показывать записи только для рассылок текущего пользователя.
        Менеджеры видят весь журнал."""
        if self.request.user.is_staff:
            return Mailjurnal.objects.all()
        # Используем поле 'user' для Mailjurnal, так как у него нет 'owner'
        return Mailjurnal.objects.filter(user=self.request.user)

# Представления для активации/приостановки/завершения рассылок
class MailingActivateView(LoginRequiredMixin, View):
    """
    Представление для активации рассылки (установка статуса 'running').
    Менеджер может активировать любую рассылку, обычный пользователь - только свою.
    """
    def get(self, request, pk):
        if self.request.user.is_staff:
            mailing = get_object_or_404(Mailing, pk=pk)
        else:
            # Используем 'owner' для фильтрации
            mailing = get_object_or_404(Mailing, pk=pk, owner=self.request.user)
        mailing.status = 'running'
        mailing.save()
        messages.success(request, f'Рассылка "{mailing.title}" успешно активирована.')
        return redirect('mailing:mailing_list')

class MailingPauseView(LoginRequiredMixin, View):
    """
    Преставление для приостновки рассылки (установка статуса 'paused').
    Менеджер может приостановить любую рассылку, обычный пользователь - только свою.
    """
    def get(self, request, pk):
        if self.request.user.is_staff:
            mailing = get_object_or_404(Mailing, pk=pk)
        else:

            mailing = get_object_or_404(Mailing, pk=pk, owner=self.request.user)
        mailing.status = 'paused'
        mailing.save()
        messages.success(request, f'Рассылка "{mailing.title}" успешно приостановлена.')
        return redirect('mailing:mailing_list')

class MailingDeactivateView(LoginRequiredMixin, View):

    def get(self, request, pk):
        if self.request.user.is_staff:
            mailing = get_object_or_404(Mailing, pk=pk)
        else:

            mailing = get_object_or_404(Mailing, pk=pk, owner=self.request.user)
        mailing.status = 'completed'
        mailing.save()
        messages.success(request, f'Рассылка "{mailing.title}" успешно завершена.')
        return redirect('mailing:mailing_list')

class MailingReportListView(LoginRequiredMixin, ListView):
    model = MailingReport
    template_name = 'mailing/report_list.html'
    context_object_name = 'reports'

    def get_queryset(self):
        """Фильтрация отчетов по текущему пользователю. Менеджеры видят все отчеты."""
        if self.request.user.is_staff:
            return MailingReport.objects.all()

        return MailingReport.objects.filter(user=self.request.user)
