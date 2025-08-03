from django.utils import timezone
from django.db import models

from users.models import Users


class Client(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=300, help_text='Введите Фамилию, имя, отчество', verbose_name='ФИО')
    comment = models.TextField(help_text='Комментарии',null=True, blank=True, verbose_name="Комментарии")
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='clients')
#Обязательные для заполнения
    def __str__(self):
        return f'{self.full_name} ({self.email})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

class Message(models.Model):

    topic_message = models.CharField(max_length=300, help_text='Введите тему письма', verbose_name='Тема письма')
    text_message = models.TextField(help_text='Введите текст письма', verbose_name="Текс пиcьма")
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='messages')
    def __str__(self):
        return f'{self.topic_message}'
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

#Создаю новую модель для рассылок

class Mailing(models.Model):
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
    abonent = models.ManyToManyField("Client", verbose_name='Получатели')

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

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
    malling = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')
    client = models.ForeignKey('Client', on_delete=models.CASCADE, verbose_name='Получатель', blank=True, null=True)

    class Meta:
        verbose_name = 'Журнал рассылки'
        verbose_name_plural = 'Журналы рассылок'

    def __str__(self):
        # Статус и время попытки
        return f"{self.get_status_display()} в {self.time_malling.strftime('%Y-%m-%d %H:%M:%S')}"

