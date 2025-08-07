from django.core.management import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.db import transaction

from mailing.models import Mailing, Mailjurnal, MailingReport


class Command(BaseCommand):
    """
    Команда для запуска рассылок.
    """
    help = 'Запускает рассылки, которые соответствуют расписанию.'

    def handle(self, *args, **options):
        now = timezone.now()
        active_mailings = Mailing.objects.filter(
            start_time__lte=now,
            end_time__gt=now,
            status='running'
        )
        self.stdout.write(self.style.SUCCESS(f'Найдено {active_mailings.count()} активных рассылок.'))

        for mailing in active_mailings:
            recipients = mailing.abonent.all()
            if not recipients:
                self.stdout.write(self.style.WARNING(f'Рассылка "{mailing.title}" не имеет получателей.'))
                continue

            with transaction.atomic():
                successful_count = 0
                unsuccessful_count = 0

                # Создаем журнал для каждого получателя
                for client in recipients:
                    try:
                        send_mail(
                            subject=mailing.message.topic_message,
                            message=mailing.message.text_message,
                            from_email=settings.EMAIL_HOST_USER,
                            recipient_list=[client.email],
                            fail_silently=False,
                        )

                        Mailjurnal.objects.create(
                            malling=mailing,
                            client=client,
                            status='успешно',
                            server_response='Письмо успешно отправлено',
                            user=mailing.user
                        )
                        successful_count += 1
                        self.stdout.write(self.style.SUCCESS(
                            f'Успешно отправлено письмо клиенту {client.email} для рассылки "{mailing.title}".'))
                    except Exception as e:
                        Mailjurnal.objects.create(
                            malling=mailing,
                            client=client,
                            status='не_успешно',
                            server_response=str(e),
                            user=mailing.user
                        )
                        unsuccessful_count += 1
                        self.stdout.write(self.style.ERROR(
                            f'Ошибка отправки письма клиенту {client.email} для рассылки "{mailing.title}": {e}'))

                # Создаем или обновляем отчет для этой рассылки
                MailingReport.objects.update_or_create(
                    mailing=mailing,
                    user=mailing.user,
                    defaults={
                        'successful_attempts': successful_count,
                        'unsuccessful_attempts': unsuccessful_count,
                    }
                )
                self.stdout.write(self.style.SUCCESS(
                    f'Отчет для рассылки "{mailing.title}" обновлен/создан. '
                    f'Успешно: {successful_count}, Неуспешно: {unsuccessful_count}'))

        self.stdout.write(self.style.SUCCESS('Проверка рассылок завершена.'))
