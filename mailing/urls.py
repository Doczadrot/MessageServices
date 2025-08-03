from django.urls import path
from mailing.views import (
    MessageListView, MessageDetailView, MessageUpdateView, MessageDeleteView, MessageCreateView,
    ClientCreateView, ClientListView, ClientDetailView, ClientUpdateView, ClientDeleteView,
    MailingDeleteView, MailingUpdateView, MailingDetailView, MailingListView, MailingCreateView,
    MailingSendView, MailjurnalListView, MailingActivateView, MailingPauseView, MailingDeactivateView)


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

    # URL-ы для рассылок
    path('mailings/create/', MailingCreateView.as_view(), name='create_mailing'),
    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('mailings/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailings/update/<int:pk>/', MailingUpdateView.as_view(), name='update_mailing'),
    path('mailings/delete/<int:pk>/', MailingDeleteView.as_view(), name='delete_mailing'),
    # Ceрвисный URL
    path('mailings/send/<int:pk>/', MailingSendView.as_view(), name='send_mailing'),
    # URL-адрес для журнала рассылок
    path('mailjurnal/', MailjurnalListView.as_view(), name='mailjurnal_list'),
    path('mailings/activate/<int:pk>/', MailingActivateView.as_view(), name='activate_mailing'),
    path('mailings/pause/<int:pk>/', MailingPauseView.as_view(), name='pause_mailing'),
    path('mailings/deactivate/<int:pk>/', MailingDeactivateView.as_view(), name='deactivate_mailing'),
]