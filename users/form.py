from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from users.models import Users


class UsersRegisterForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ('email', 'username', 'country', 'phone_number', 'image')

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'


class LoginForm(AuthenticationForm):
    class Meta:
        fields = ['username', 'password']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'
