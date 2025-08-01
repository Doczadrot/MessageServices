from django.contrib import admin
from .models import Client, Message, Malling, Mailjurnal # Импортируем все модели

# Регистрация моделей в админ-панели Django
admin.site.register(Client)
admin.site.register(Message)
admin.site.register(Malling)
admin.site.register(Mailjurnal)