from django.utils import timezone
from django.db import models

class LinkService(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=300, help_text='Введите Фамилию, имя, отчество', verbose_name='ФИО')
    comment = models.TextField(help_text='Комментарии',null=True, blank=True)

#Обязательные для заполнения
    def __str__(self):
        return f'{self.full_name} ({self.email})'

class Message(models.Model):
    topic_message = models.CharField(max_length=300, help_text='Введите тему письма', verbose_name='Тема письма')
    text_message = models.TextField(help_text='Введите текст письма', verbose_name="Текс пиcьма")

    def __str__(self):
        return f'{self.topic_message}'

#Создаю новую модель для рассылок

class Malling(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Ежедневно'),
        ('weekly', 'Еженедельно'),
        ('monthly', 'Ежемесячно'),
    ]

    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('running', 'Запущена'),
        ('completed', 'Завершена'),
    ]

    title = models.CharField(max_length=100, verbose_name='Название рассылки')
    start_time = models.DateTimeField(default=timezone.now, verbose_name='Время начала')
    end_time = models.DateTimeField(default=timezone.now, verbose_name='Время окончания')
    periodicity = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, verbose_name='Периодичность') #периодичность
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,  verbose_name='Статус')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Cообщение')
    abonent = models.ManyToManyField("LinkService", verbose_name='Получатели')

    def __str__(self):
        return self.title

class Mailjurnal(models.Model):

    STATUS_CHOICES = [
        ('успешно', 'Успешно'),
        ('не_успешно', 'Не успешно'),
    ]
    time_malling = models.DateTimeField(auto_now_add=True, verbose_name='Время попытки рассылки')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='статус рассылки')
    server_response = models.TextField(null=True, blank=True, verbose_name='Ответ сервера')
    malling = models.ForeignKey(Malling, on_delete=models.CASCADE, verbose_name='Рассылка')

    def __str__(self):
        # Статус и время попытки
        return f"{self.get_status_display()} в {self.time_malling.strftime('%Y-%m-%d %H:%M:%S')}"




