from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель создания и регистрации пользователя"""
    email = models.EmailField(unique=True, verbose_name='Ваша почта')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name='Номер телефона')
    avatar = models.ImageField(upload_to='users/avatars/', blank=True, null=True, verbose_name='Фото(необязательно)')
    country = models.CharField(max_length=50, blank=True, verbose_name='Страна проживания')
    token = models.CharField(max_length=100, verbose_name="Токен", blank=True, null=True,)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
            ('can_block_user', 'can block user'),
            ('can_stop_mailing', 'can stop mailing')
        ]
