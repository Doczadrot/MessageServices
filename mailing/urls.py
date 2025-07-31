from django.urls import path

from mailing.views import MessageListView, MessageDetailView, MessageUpdateView, MessageDeleteView, MessageCreateView

app_name = 'mailing'

urlpatterns = [
    path('create/', MessageCreateView.as_view(), name='create_message'),
    path('', MessageListView.as_view(), name='message_list'),
    path('<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('update/<int:pk>/', MessageUpdateView.as_view(), name='update_message'),
    path('delete/<int:pk>/', MessageDeleteView.as_view(), name='delete_message'),
]