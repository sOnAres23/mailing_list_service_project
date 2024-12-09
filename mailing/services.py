from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail


from django.utils import timezone

from config.settings import CACHE_ENABLE
from mailing.models import Mailing, MailingAttempt


def send_mailing(self):
    """Функция для отправки рассылки"""
    email = [recipients.email for recipients in self.object.recipients.all()]

    self.object.first_sending = timezone.now()
    self.object.status = 'Запущена'
    self.object.save()

    server_response = send_mail(
        subject=f'{self.object.message.theme}',
        message=f'{self.object.message.content}',
        recipient_list=email,
        fail_silently=False,
        from_email=settings.EMAIL_HOST_USER
    )

    self.object.end_sending = timezone.now()
    self.object.status = 'Завершена'
    self.object.save()

    mailing_attempt = MailingAttempt.objects.create(mailing=self.object, server_response=server_response,
                                                    owner=self.request.user)
    if server_response:
        mailing_attempt.status = 'Успешно'
    else:
        mailing_attempt.status = 'Не успешно'
    mailing_attempt.save()


def get_mailing_from_cache():
    """Получение данных по рассылкам из кэша, если кэш пуст берем из БД"""
    if not CACHE_ENABLE:
        return Mailing.objects.all()
    key = "mailing_list"
    cache_data = cache.get(key)
    if cache_data is not None:
        return cache_data
    cache_data = Mailing.objects.all()
    cache.set(key, cache_data)
    return cache_data
