from django.urls import path

from config.urls import urlpatterns
from users.form import UsersRegisterForm

app_name = 'users'

urlpatterns = [
    path('register/', UsersRegisterFormView)
]
