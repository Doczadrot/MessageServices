import pytz
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings
from mailing.models import Mailjurnal, Mailing


def send_mailing(mailing_object):
    """
    Отправляет письма для одной рассылки и записывает результат в журнал.
    Принимает объект рассылки (Mailing).
    """
    timezone = pytz.timezone(settings.TIME_ZONE)
    now = timezone.localize(datetime.now())

    for abonent in mailing_object.abonent.all():
        try:
            send_mail(
                subject=mailing_object.message.topic_message,
                message=mailing_object.message.text_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[abonent.email],
                fail_silently=False
            )
            # Создаем запись в журнале об успешной отправке
            Mailjurnal.objects.create(
                time_malling=now,
                status='успешно',
                malling=mailing_object,
                client=abonent,
                server_response=f'Письмо успешно отправлено клиенту {abonent.email}'
            )
        except Exception as e:
            # Создаем запись в журнале об ошибке
            Mailjurnal.objects.create(
                time_malling=now,
                status='не_успешно',
                malling=mailing_object,
                client=abonent,
                server_response=f'Ошибка при отправке: {e}'
            )

    return