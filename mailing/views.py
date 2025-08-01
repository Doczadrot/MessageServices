from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView

from mailing.models import Message, Client


class MessageCreateView(CreateView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')
    fields = ['topic_message', 'text_message']

class MessageListView(ListView):
    model = Message
    context_object_name = 'messages'
    template_name = 'mailing/mailing_list.html'

class MessageUpdateView(UpdateView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')
    fields = ['topic_message', 'text_message']

class MessageDetailView(DetailView):
    model = Message
    context_object_name = 'message'

class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')
    template_name = 'mailing/message_confirm_delete.html'

class ClientCreateView(CreateView):
    model = Client
    fields = ['email', 'full_name', 'comment']
    success_url = reverse_lazy('mailing:client_list')

class ClientUpdateView(UpdateView):
    model = Client
    fields = ['email', 'full_name', 'comment']
    success_url = reverse_lazy('mailing:client_list')

class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')
    template_name = 'mailing/client_confirm_delete.html'

class ClientDetailView(DetailView):
    model = Client
    context_object_name = 'client'

class ClientListView(ListView):
    model = Client
    context_object_name = 'clients'
    template_name = 'mailing/client_list.html'













