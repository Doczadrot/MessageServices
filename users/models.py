from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email должен быть установлен')
        email = self.normalize_email(email)
        extra_fields.setdefault('username', email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        extra_fields['username'] = email

        return self.create_user(email, password, **extra_fields)

class Users(AbstractUser):
    email = models.EmailField(unique=True)
    country = models.CharField(unique=False, verbose_name='Страна', help_text='Введите страну')
    image = models.ImageField(upload_to='users/avatar', verbose_name='AVATAR', blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True, unique=True, help_text="Введите номер телефона в международном формате")
    #Поля для подтверждения почты
    email_verify = models.BooleanField(default=True, verbose_name='Проверка почты')
    token = models.CharField(max_length=100, blank=True, null=True, verbose_name='Токен')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


