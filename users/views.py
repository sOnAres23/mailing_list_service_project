import secrets

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView

from config import settings
from users.forms import CustomUserCreationForm, UserUpdateForm
from users.models import User


class UserRegisterView(CreateView):
    model = User
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:email_confirmation")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        login(self.request, user)
        token = secrets.token_hex(16)
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        user.token = token
        user.save()
        message = 'Добро пожаловать в сервис^_^ Спасибо, что зарегистрировались на нашем сайте!'
        send_mail(
            subject="Подтверждение почты",
            message=f"{message} Перейдите по ссылке для подтверждения почты: {url} ",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "users/user_list.html"


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    form_class = UserUpdateForm

    def get_object(self, queryset=None):
        user = self.request.user
        self.object = super().get_object(queryset)
        if user.is_superuser:
            return self.object
        raise PermissionDenied


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return reverse_lazy("users:users")
        else:
            return reverse_lazy("mailing:home")

    def get_object(self, queryset=None):
        user = self.request.user
        self.object = super().get_object(queryset)
        if user.is_superuser:
            return self.object
        raise PermissionDenied


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return reverse_lazy("users:users")
        else:
            return reverse_lazy("mailing:home")

    def get_object(self, queryset=None):
        user = self.request.user
        self.object = super().get_object(queryset)
        if user.is_superuser:
            return self.object
        raise PermissionDenied


class EmailConfirmationView(TemplateView):
    model = User
    template_name = "users/email_confirmation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Письмо активации отправлено на вашу почту:)"
        return context


# class PasswordRecoveryView(FormView):
#     template_name = "users/password_recovery.html"
#     form_class = PasswordRecoveryForm
#     success_url = reverse_lazy("users:login")
#
#     def form_valid(self, form):
#         email = form.cleaned_data["email"]
#         user = User.objects.get(email=email)
#         length = 12
#         alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
#         password = get_random_string(length, alphabet)
#         user.set_password(password)
#         user.save()
#         send_mail(
#             subject="Восстановление пароля",
#             message=f"Ваш новый пароль: {password}",
#             from_email=settings.EMAIL_HOST_USER,
#             recipient_list=[user.email],
#             fail_silently=False,
#         )
#         return super().form_valid(form)
