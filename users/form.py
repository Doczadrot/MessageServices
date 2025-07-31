from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from users.models import Users


class UsersRegisterForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ('email', 'username', 'country', 'phone_number', 'image')

class LoginForm(AuthenticationForm):
    class Meta:
        fields = ['username', 'password']

