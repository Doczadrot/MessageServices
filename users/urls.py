from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from users.views import UserRegisterView, UserLoginView, VerifyEmailView

app_name = 'users'

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name = 'register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='users:login'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),
]
