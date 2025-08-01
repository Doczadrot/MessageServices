from django.urls import path

from mailing.views import MessageListView, MessageDetailView, MessageUpdateView, MessageDeleteView, MessageCreateView, \
    ClientCreateView, ClientListView, ClientDetailView, ClientUpdateView, ClientDeleteView

app_name = 'mailing'

urlpatterns = [
    # URL-ы для сообщений
    path('messages/create/', MessageCreateView.as_view(), name='create_message'),
    path('messages/', MessageListView.as_view(), name='message_list'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('messages/update/<int:pk>/', MessageUpdateView.as_view(), name='update_message'),
    path('messages/delete/<int:pk>/', MessageDeleteView.as_view(), name='delete_message'),

    # URL-ы для клиентов
    path('clients/create/', ClientCreateView.as_view(), name='create_client'),
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('clients/update/<int:pk>/', ClientUpdateView.as_view(), name='update_client'),
    path('clients/delete/<int:pk>/', ClientDeleteView.as_view(), name='delete_client'),
]