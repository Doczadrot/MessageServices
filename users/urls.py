from django.contrib.auth.views import LogoutView
from django.urls import path

from config.urls import urlpatterns
from users.views import UserRegisterView, UserLoginView

app_name = 'users'

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name = 'register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='users:login'), name='logout')
]
