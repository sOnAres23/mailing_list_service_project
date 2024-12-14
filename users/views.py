import secrets

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.utils.crypto import get_random_string
from django.views.generic import CreateView, ListView, DetailView, UpdateView, TemplateView, FormView

from config import settings
from users.forms import CustomUserCreationForm, UserUpdateForm, PasswordRecoveryForm
from users.models import User


class UserRegisterView(CreateView):
    """Класс для регистрации пользователя"""
    model = User
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:email_confirmation")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        message = 'Добро пожаловать в сервис^_^ Спасибо, что зарегистрировались на нашем сайте!'
        send_mail(
            subject="Подтверждение почты",
            message=f"{message} Перейдите по ссылке для подтверждения почты: {url} ",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


class UserListView(LoginRequiredMixin, ListView):
    """Класс для отображения всех пользователей сайта"""
    model = User
    template_name = "users/user_list.html"

    def handle_permission(self):
        return self.request.user.groups.filter(name="Менеджеры").exists() or self.request.user.is_superuser


class UserDetailView(LoginRequiredMixin, DetailView):
    """Класс для отображения детальной информации о пользователе"""
    model = User
    form_class = UserUpdateForm
    context_object_name = 'user'


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """Класс для редактирования профиля пользователя"""
    model = User
    form_class = UserUpdateForm
    template_name = 'users/register.html'

    def get_success_url(self):
        return reverse("users:detail", args=[self.kwargs.get("pk")])


class EmailConfirmationView(TemplateView):
    """Класс для отображения отправки письма подтверждения"""
    model = User
    template_name = "users/email_confirmation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Письмо активации отправлено на вашу почту:)"
        return context


class PasswordConfirmationView(TemplateView):
    """Класс для отображения отправки письма о пароле на почту"""
    model = User
    template_name = "users/password-confirmation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Письмо по восстановлению отправлено на вашу почту:)"
        return context


class PasswordRecoveryView(FormView):
    """Класс для восстановления пароля"""
    template_name = "users/password_recovery.html"
    form_class = PasswordRecoveryForm
    success_url = reverse_lazy("users:password-confirmation")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        user = User.objects.get(email=email)
        length = 12
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        password = get_random_string(length, alphabet)
        user.set_password(password)
        user.save()
        send_mail(
            subject="Восстановление пароля",
            message=f"Ваш новый пароль: {password}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return super().form_valid(form)
