from django.db import models

from users.models import User


class RecipientMailing(models.Model):
    """Модель создания Получателя рассылки"""
    email = models.EmailField(max_length=150, unique=True, verbose_name="Почта")
    fio = models.CharField(max_length=150, verbose_name="Ф.И.О.")
    comment = models.TextField(max_length=255, blank=True, null=True, verbose_name="Комментарий")
    photo = models.ImageField(upload_to="mailing/photos", blank=True, null=True, verbose_name="Фотография")
    is_active = models.BooleanField(default=True, verbose_name="Активность")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Владелец")

    def __str__(self):
        return f"{self.fio} <{self.email}>"

    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылки"
        ordering = ["fio"]


class Message(models.Model):
    """Модель создания Сообщения"""
    theme = models.CharField(max_length=255, verbose_name="Тема сообщения")
    content = models.TextField(max_length=800, verbose_name="Содержание сообщения")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Владелец")

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["theme"]


class Mailing(models.Model):
    """Модель создания Рассылки"""
    CREATED = "Создана"
    LAUNCHED = "Запущена"
    COMPLETED = "Завершена"

    STATUS_CHOICES = [
        (CREATED, "Создана"),
        (LAUNCHED, "Запущена"),
        (COMPLETED, "Завершена"),
    ]

    first_sending = models.DateTimeField(verbose_name="Дата и время первого отправления")
    end_sending = models.DateTimeField(verbose_name="Дата и время окончания отправки")
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=CREATED,
        verbose_name="Статус рассылки"
    )
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="Сообщение", related_name="mailings")
    recipients = models.ManyToManyField(RecipientMailing, related_name="recipients", verbose_name="Получатели",
                                        help_text="Укажите получателей рассылки (используйте CTRL или COMMAND)",)
    is_active = models.BooleanField(default=True, verbose_name="Активность")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Владелец")

    def __str__(self):
        return f"Рассылка {self.id}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["first_sending"]


class MailingAttempt(models.Model):
    """Модель создания Попытки отправки рассылки"""

    STATUS_OK = "Успешно"
    STATUS_NOK = "Не успешно"

    STATUS_CHOICES = [
        (STATUS_OK, "Успешно"),
        (STATUS_NOK, "Не успешно"),
    ]

    date_attempt = models.DateTimeField(verbose_name="Дата и время попытки рассылки")
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        verbose_name="Статус попытки"
    )
    server_response = models.TextField(max_length=150, verbose_name="Ответ почтового сервера")
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name="Рассылка", related_name="mailing")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Владелец")

    def __str__(self):
        return f"{self.date_attempt} <{self.status}>"

    class Meta:
        verbose_name = "Попытка"
        verbose_name_plural = "Попытки"
        ordering = ["date_attempt", "status"]