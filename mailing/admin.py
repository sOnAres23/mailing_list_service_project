from django.contrib import admin

from mailing.models import Mailing, MailingAttempt, Message, RecipientMailing
from users.models import User


@admin.register(RecipientMailing)
class RecipientMailingAdmin(admin.ModelAdmin):
    list_display = ("id", "fio", "email", "comment", "owner")
    list_filter = ("fio",)
    search_fields = ("fio", "email",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "theme", "content", "owner")
    search_fields = ("theme",)
    list_filter = ("theme",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("id", "first_sending", "end_sending", "status", "message", "owner")
    search_fields = ("status",)
    list_filter = ("status",)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "avatar", "email", "first_name", "last_name", "middle_name", "phone_number", "country")
    search_fields = ("email",)
    list_filter = ("email",)


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "date_attempt", "status")
    search_fields = ("owner",)
    list_filter = ("owner",)
