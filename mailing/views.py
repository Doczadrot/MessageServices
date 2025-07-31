from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView

from mailing.models import Message


class MessageCreateView(CreateView):
    model = Message
    success_url = reverse_lazy('message_list')
    fields = ['topic_message', 'text_message']

class MessageListView(ListView):
    model = Message
    context_object_name = 'messages'
    template_name = 'mailing/mailing_list.html'

class MessageUpdateView(UpdateView):
    model = Message
    success_url = reverse_lazy('message_list')
    fields = ['topic_message', 'text_message']

class MessageDetailView(DetailView):
    model = Message
    context_object_name = 'message'

class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('message_list')
    template_name = 'mailing/message_confirm_delete.html'









