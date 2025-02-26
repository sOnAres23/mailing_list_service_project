from django.urls import path
from django.views.decorators.cache import cache_page

from mailing import views

app_name = 'mailing'

urlpatterns = [path("home/", views.IndexView.as_view(), name="home"),
               path("contacts/", views.ContactsTemplateView.as_view(), name="contacts"),
               path("recipientmailings/", views.RecipientMailingListView.as_view(),
                    name="recipientmailing_list"),
               path("recipientmailing/<int:pk>/detail/", cache_page(60)(views.RecipientMailingDetailView.as_view()),
                    name="recipientmailing_detail"),
               path("recipientmailing/create/", views.RecipientMailingCreateView.as_view(),
                    name="recipientmailing_create"),
               path("recipientmailing/<int:pk>/update/", views.RecipientMailingUpdateView.as_view(),
                    name="recipientmailing_update"),
               path("recipientmailing/<int:pk>/delete/", views.RecipientMailingDeleteView.as_view(),
                    name="recipientmailing_delete", ),
               path("messages/", cache_page(60)(views.MessageListView.as_view()), name="message_list"),
               path("message/<int:pk>/detail/", cache_page(60)(views.MessageDetailView.as_view()),
                    name="message_detail"),
               path("message/create/", views.MessageCreateView.as_view(), name="message_create"),
               path("message/<int:pk>/update/", views.MessageUpdateView.as_view(), name="message_update"),
               path("message/<int:pk>/delete/", views.MessageDeleteView.as_view(), name="message_delete"),
               path("mailings/", views.MailingListView.as_view(), name="mailing_list"),
               path("mailing/<int:pk>/detail/", cache_page(60)(views.MailingDetailView.as_view()),
                    name="mailing_detail"),
               path("mailing/create/", views.MailingCreateView.as_view(), name="mailing_create"),
               path("mailing/<int:pk>/update/", views.MailingUpdateView.as_view(), name="mailing_update"),
               path("mailing/<int:pk>/delete/", views.MailingDeleteView.as_view(), name="mailing_delete"),
               path("<int:pk>/mailing_send/", views.MailingSendView.as_view(), name="mailing_send"),
               path("<int:pk>/mailing_stop/", views.MailingStopSendView.as_view(), name="mailing_stop"),
               path("attempts/", cache_page(60)(views.MailingAttemptListView.as_view()), name="attempt"),
               ]
