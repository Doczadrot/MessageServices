import pytz
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings
from mailing.models import Mailjurnal, Mailing, MailingReport  # Импортируем MailingReport


def send_mailing(mailing_object):
    """
    Отправляет письма для одной рассылки и записывает результат в журнал.
    Принимает объект рассылки (Mailing).
    """
    timezone = pytz.timezone(settings.TIME_ZONE)
    now = timezone.localize(datetime.now())

    successful_attempts = 0
    unsuccessful_attempts = 0

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
                server_response=f'Письмо успешно отправлено клиенту {abonent.email}',
                user=mailing_object.owner
            )
            successful_attempts += 1
        except Exception as e:
            # Создаем запись в журнале об ошибке
            Mailjurnal.objects.create(
                time_malling=now,
                status='не_успешно',
                malling=mailing_object,
                client=abonent,
                server_response=f'Ошибка при отправке: {e}',
                user=mailing_object.owner
            )
            unsuccessful_attempts += 1

    # После отправки всех писем, создаем или обновляем отчет
    MailingReport.objects.update_or_create(
        mailing=mailing_object,
        user=mailing_object.owner,
        defaults={
            'successful_attempts': successful_attempts,
            'unsuccessful_attempts': unsuccessful_attempts,
        }
    )

    return