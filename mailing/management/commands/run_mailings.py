import pytz
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from mailing.models import Mailing, Mailjurnal


class Command(BaseCommand):
    help = 'Запускает рассылки по расписанию'

    def handle(self, *args, **kwargs):
        # 1. Получаем текущее время с учетом часового пояса
        timezone = pytz.timezone(settings.TIME_ZONE)
        now = timezone.localize(datetime.now())

        # 2. Находим активные рассылки
        active_mailings = Mailing.objects.filter(
            status='running',
            start_time__lte=now,
            end_time__gte=now
        )

        for mailing in active_mailings:
            # 3. Проверяем, нужно ли отправлять письмо
            last_sent = Mailjurnal.objects.filter(
                malling=mailing,
                status='успешно'
            ).order_by('-time_malling').first()

            should_send = False
            if not last_sent:
                should_send = True
            else:
                time_difference = now - last_sent.time_malling
                if mailing.periodicity == 'daily' and time_difference >= timedelta(days=1):
                    should_send = True
                elif mailing.periodicity == 'weekly' and time_difference >= timedelta(weeks=1):
                    should_send = True
                elif mailing.periodicity == 'monthly' and time_difference >= timedelta(days=30):
                    should_send = True

            # 4. Если нужно отправить, то отправляем
            if should_send:
                for abonent in mailing.abonent.all():
                    try:
                        send_mail(
                            subject=mailing.message.topic_message,
                            message=mailing.message.text_message,
                            from_email=settings.EMAIL_HOST_USER,
                            recipient_list=[abonent.email],
                            fail_silently=False
                        )
                        Mailjurnal.objects.create(
                            time_malling=now,
                            status='успешно',
                            malling=mailing,
                            client=abonent,
                            server_response=f'Письмо успешно отправлено клиенту {abonent.email}'
                        )
                        self.stdout.write(self.style.SUCCESS(
                            f'Письмо успешно отправлено клиенту {abonent.email} для рассылки "{mailing.title}"'))
                    except Exception as e:
                        Mailjurnal.objects.create(
                            time_malling=now,
                            status='не_успешно',
                            malling=mailing,
                            client=abonent,
                            server_response=f'Ошибка при отправке: {e}'
                        )
                        self.stdout.write(self.style.ERROR(f'Ошибка отправки для клиента {abonent.email}: {e}'))

        # 5. Обновляем статус рассылок, которые завершились
        completed_mailings = Mailing.objects.filter(
            status='running',
            end_time__lt=now
        )
        for mailing in completed_mailings:
            mailing.status = 'completed'
            mailing.save()
            self.stdout.write(self.style.SUCCESS(f'Рассылка "{mailing.title}" завершена.'))

        self.stdout.write(self.style.SUCCESS('Проверка рассылок завершена.'))