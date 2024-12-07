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


class IndexView(TemplateView):
    template_name = "mailing/home.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["title"] = "Главная"
        context_data["count_mailing"] = len(Mailing.objects.all())
        active_mailings_count = Mailing.objects.filter(status="Запущена").count()
        context_data["active_mailings_count"] = active_mailings_count
        unique_clients_count = RecipientMailing.objects.distinct().count()
        context_data["unique_clients_count"] = unique_clients_count
        return context_data


class RecipientMailingCreateView(LoginRequiredMixin, CreateView):
    model = RecipientMailing
    form_class = RecipientForm
    success_url = reverse_lazy("mailing:recipient_list")

    def form_valid(self, form):
        recipient = form.save()
        recipient.owner = self.request.user
        recipient.save()

        return super().form_valid(form)


class RecipientMailingListView(ListView):
    model = RecipientMailing
    context_object_name = "recipients"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["title"] = "Получатели"
        return context_data

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name="Менеджеры"):
            return super().get_queryset()
        elif user.groups.filter(name="Пользователи"):
            return super().get_queryset().filter(owner=self.request.user)
        raise PermissionDenied


class RecipientMailingDetailView(LoginRequiredMixin, DetailView):
    model = RecipientMailing
    form_class = RecipientForm

    def dispatch(self, request, queryset=None, *args, **kwargs):
        user = self.request.user
        self.object = super().get_object(queryset)
        if user.is_superuser or user.groups.filter(name="Менеджеры"):
            return self.object
        if self.object.owner != user and not user.is_superuser:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class RecipientMailingUpdateView(LoginRequiredMixin, UpdateView):
    model = RecipientMailing
    form_class = RecipientForm
    success_url = reverse_lazy("mailing:recipient_list")

    def dispatch(self, request, queryset=None, *args, **kwargs):
        user = self.request.user
        self.object = super().get_object(queryset)
        if self.object.owner != user and not user.is_superuser:
            return HttpResponseForbidden("У вас нет прав для редактирования!")
        return super().dispatch(request, *args, **kwargs)


class RecipientMailingDeleteView(LoginRequiredMixin, DeleteView):
    model = RecipientMailing
    success_url = reverse_lazy("mailing:recipient_list")

    def dispatch(self, request, queryset=None, *args, **kwargs):
        user = self.request.user
        self.object = super().get_object(queryset)
        if self.object.owner != user and not user.is_superuser:
            return HttpResponseForbidden("У вас нет прав для удаления!")
        return super().dispatch(request, *args, **kwargs)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")

    def form_valid(self, form):
        message = form.save()
        message.owner = self.request.user
        message.save()

        return super().form_valid(form)


class MessageListView(ListView):
    model = Message
    context_object_name = "messages"

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if user.is_superuser:
            return super().get_queryset()
        else:
            raise PermissionDenied


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    form_class = MessageForm

    def get_object(self, queryset=None):
        user = self.request.user
        self.object = super().get_object(queryset)
        if not user.is_superuser:
            raise PermissionDenied
        return self.object


class MessageUpdateView(LoginRequiredMixin, UpdateView):
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
    model = Message
    success_url = reverse_lazy("mailing:message_list")

    def dispatch(self, request, queryset=None, *args, **kwargs):
        user = self.request.user
        self.object = super().get_object(queryset)
        if self.object.owner != user and not user.is_superuser:
            return HttpResponseForbidden("У вас нет прав для удаления!")
        return super().dispatch(request, *args, **kwargs)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailing:mailing_list")

    def form_valid(self, form):
        mailing = form.save()
        mailing.owner = self.request.user
        mailing.save()

        return super().form_valid(form)


class MailingListView(ListView):
    model = Mailing
    context_object_name = "mailings"

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name="Менеджеры").exists():
            return super().get_queryset()
        elif user.groups.filter(name="Пользователи").exists():
            return super().get_queryset().filter(owner=self.request.user)
        raise PermissionDenied


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    form_class = MailingForm

    def get_object(self, queryset=None):
        user = self.request.user
        self.object = super().get_object(queryset)
        if user.groups.filter(name="Менеджеры") or user.is_superuser:
            return self.object
        if self.object.owner != user and not user.is_superuser:
            raise PermissionDenied
        return self.object


class MailingUpdateView(LoginRequiredMixin, UpdateView):
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
    model = Mailing
    success_url = reverse_lazy("mailing:mailing_list")

    def dispatch(self, request, queryset=None, *args, **kwargs):
        user = self.request.user
        self.object = super().get_object(queryset)
        if self.object.owner != user and not user.is_superuser:
            return HttpResponseForbidden("У вас нет прав для удаления!")
        return super().dispatch(request, *args, **kwargs)


class MailingStopSendView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "mailing_service/mailing_stop.html"
    context_object_name = "mailing_stop"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.has_perm("can_stop_mailing"):
            self.object.status = "Отключена"
            self.object.save()
        return self.object


class MailingAttemptCreateView(LoginRequiredMixin, CreateView):
    model = MailingAttempt

    def form_valid(self, form):
        mailingattempt = form.save()
        mailingattempt.owner = self.request.user
        mailingattempt.save()

        return super().form_valid(form)


class MailingAttemptListView(LoginRequiredMixin, ListView):
    model = MailingAttempt
    context_object_name = "attempts"

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if user.is_superuser:
            return super().get_queryset()
        elif user.groups.filter(name="Пользователи").exists():
            return super().get_queryset().filter(owner=self.request.user)
        raise PermissionDenied


class ContactsTemplateView(TemplateView):
    """Класс для представления страницы обратной связи"""
    template_name = "mailing/contacts.html"

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
        return render(request, 'catalog/contacts.html')
