import smtplib

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView, TemplateView

from mailing.forms import RecipientForm, MessageForm, MailingForm
from mailing.models import RecipientMailing, Message, Mailing, MailingAttempt
from mailing.services import send_mailing, get_mailing_from_cache


class IndexView(TemplateView):
    """Класс для отображения главной страницы"""
    template_name = "mailing/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context["user_mail"] = RecipientMailing.objects.all()
        context["mailing_all_started"] = Mailing.objects.filter(status="Запущена")
        context["mailings"] = Mailing.objects.all()

        if user.is_authenticated:
            context['user_usermail'] = RecipientMailing.objects.filter(owner=user)
            context['user_mailing_started'] = Mailing.objects.filter(owner=user, status="Запущена")
            context['user_mailings'] = Mailing.objects.filter(owner=user)

        return context

    @staticmethod
    def get_queryset(self):
        """Настройка серверного кэширования главной страницы"""
        return get_mailing_from_cache()


class RecipientMailingCreateView(LoginRequiredMixin, CreateView):
    """Класс для создания получателя рассылки"""
    model = RecipientMailing
    form_class = RecipientForm
    success_url = reverse_lazy("mailing:recipientmailing_list")

    def form_valid(self, form):
        user = self.request.user
        recipient = form.save()
        recipient.owner = user
        recipient.save()

        return super().form_valid(form)


class RecipientMailingListView(ListView):
    """Класс для отображения всех получателей рассылки"""
    model = RecipientMailing

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name="Менеджеры") or user.is_superuser:
            return RecipientMailing.objects.all()
        return RecipientMailing.objects.filter(owner=user)


class RecipientMailingDetailView(LoginRequiredMixin, DetailView):
    """Класс для отображения детальной информации получателя рассылки"""
    model = RecipientMailing
    form_class = RecipientForm

    def get_object(self, queryset=None):
        user = self.request.user
        self.object = super().get_object(queryset)
        if user.groups.filter(name="Менеджеры") or user.is_superuser:
            return self.object
        if self.object.owner != user and not user.is_superuser:
            raise PermissionDenied
        return self.object


class RecipientMailingUpdateView(LoginRequiredMixin, UpdateView):
    """Класс для редактирования получателя рассылки"""
    model = RecipientMailing
    form_class = RecipientForm
    success_url = reverse_lazy("mailing:recipientmailing_list")

    def dispatch(self, request, queryset=None, *args, **kwargs):
        user = self.request.user
        self.object = super().get_object(queryset)
        if self.object.owner != user and not user.is_superuser:
            return HttpResponseForbidden("У вас нет прав для редактирования!")
        return super().dispatch(request, *args, **kwargs)


class RecipientMailingDeleteView(LoginRequiredMixin, DeleteView):
    """Класс для удаления получателя рассылки"""
    model = RecipientMailing
    success_url = reverse_lazy("mailing:recipientmailing_list")

    def dispatch(self, request, queryset=None, *args, **kwargs):
        user = self.request.user
        self.object = super().get_object(queryset)
        if self.object.owner != user and not user.is_superuser:
            return HttpResponseForbidden("У вас нет прав для удаления!")
        return super().dispatch(request, *args, **kwargs)


class MessageCreateView(LoginRequiredMixin, CreateView):
    """Класс для создания сообщения"""
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")

    def form_valid(self, form):
        user = self.request.user
        message = form.save()
        message.owner = user
        message.save()

        return super().form_valid(form)


class MessageListView(ListView):
    """Класс для отображения всех сообщений"""
    model = Message


class MessageDetailView(LoginRequiredMixin, DetailView):
    """Класс для отображения детальной информации о сообщении"""
    model = Message
    form_class = MessageForm

    def get_queryset(self):
        user = self.request.user

        if user.has_perm('mailing.can_view_message'):
            return Message.objects.all()
        return Message.objects.filter(owner=user)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """Класс для редактирования сообщения"""
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")

    def dispatch(self, request, queryset=None, *args, **kwargs):
        user = self.request.user
        self.object = super().get_object(queryset)
        if self.object.owner != user and not user.is_superuser:
            return HttpResponseForbidden("У вас нет прав для редактирования!")
        return super().dispatch(request, *args, **kwargs)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """Класс для удаления сообщения"""
    model = Message
    success_url = reverse_lazy("mailing:message_list")

    def dispatch(self, request, queryset=None, *args, **kwargs):
        user = self.request.user
        self.object = super().get_object(queryset)
        if self.object.owner != user and not user.is_superuser:
            return HttpResponseForbidden("У вас нет прав для удаления!")
        return super().dispatch(request, *args, **kwargs)


class MailingCreateView(LoginRequiredMixin, CreateView):
    """Класс для создания рассылки"""
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailing:mailing_list")

    def form_valid(self, form):
        user = self.request.user
        mailing = form.save()
        mailing.owner = user
        mailing.save()

        return super().form_valid(form)


class MailingListView(ListView):
    """Класс для отображения всех рассылок"""
    model = Mailing
    context_object_name = 'mailings'

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name="Менеджеры") or user.is_superuser:
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=user)


class MailingDetailView(LoginRequiredMixin, DetailView):
    """Класс для отображения детальной информации о рассылке"""
    model = Mailing
    form_class = MailingForm
    context_object_name = 'mailing'

    def get_object(self, queryset=None):
        user = self.request.user
        self.object = super().get_object(queryset)
        if user.groups.filter(name="Менеджеры") or user.is_superuser:
            return self.object
        if self.object.owner != user and not user.is_superuser:
            raise PermissionDenied
        return self.object


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """Класс для редактирования рассылки"""
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailing:mailing_list")

    def dispatch(self, request, queryset=None, *args, **kwargs):
        user = self.request.user
        self.object = super().get_object(queryset)
        if self.object.owner != user and not user.is_superuser:
            return HttpResponseForbidden("У вас нет прав для редактирования!")
        return super().dispatch(request, *args, **kwargs)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    """Класс для удаления рассылки"""
    model = Mailing
    success_url = reverse_lazy("mailing:mailing_list")

    def dispatch(self, request, queryset=None, *args, **kwargs):
        user = self.request.user
        self.object = super().get_object(queryset)
        if self.object.owner != user and not user.is_superuser:
            return HttpResponseForbidden("У вас нет прав для удаления!")
        return super().dispatch(request, *args, **kwargs)


class MailingSendView(LoginRequiredMixin, DetailView):
    """Класс для отправки рассылки"""
    model = Mailing
    template_name = "mailing/mailing_send.html"
    context_object_name = "mailing_send"

    def get_object(self, queryset=None):
        user = self.request.user
        self.object = super().get_object(queryset)

        if self.object.owner == user and self.object.status == "Создана":
            try:
                send_mailing(self)  # из файла services.py
            except smtplib.SMTPException as error:
                MailingAttempt.objects.create(mailing=self.object, mail_response=error, status="Не успешно")
        return self.object


class MailingStopSendView(LoginRequiredMixin, DetailView):
    """Класс для отключения рассылки"""
    model = Mailing
    template_name = "mailing/mailing_stop.html"
    context_object_name = "mailing_stop"

    def get_object(self, queryset=None):
        user = self.request.user
        self.object = super().get_object(queryset)
        if user.has_perm("can_stop_mailing"):
            self.object.status = "Отключена"
            self.object.save()
        return self.object


class MailingAttemptCreateView(LoginRequiredMixin, CreateView):
    """Класс автоматического создания попытки рассылки"""
    model = MailingAttempt

    def form_valid(self, form):
        user = self.request.user
        mailingattempt = form.save()
        mailingattempt.owner = user
        mailingattempt.save()

        return super().form_valid(form)


class MailingAttemptListView(LoginRequiredMixin, ListView):
    """Класс для отображения статистики всех рассылок"""
    model = MailingAttempt
    context_object_name = "attempts"
    template_name = "mailing/mailingattempt_list.html"

    def get_queryset(self):
        return MailingAttempt.objects.filter(owner=self.request.user)


class ContactsTemplateView(TemplateView):
    """Класс для представления страницы обратной связи"""
    template_name = "mailing/includes/contacts.html"

    def post(self, request):
        if self.request.method == 'POST':
            # Получение данных из формы
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            message = request.POST.get('message')
            # Обработка данных (для примера, отправка email)
            send_mail(f'Письмо от пользователя: {name}', f'Сообщение: {message}, Телефон для связи: {phone}',
                      settings.EMAIL_HOST_USER, ['sergeyspisak@yandex.ru'])
            # А здесь мы просто возвращаем простой ответ пользователю на сайте:
            return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
        return render(request, "mailing/includes/contacts.html")
