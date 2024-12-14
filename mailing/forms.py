from django.forms import BooleanField, ImageField, ModelForm

from mailing.models import Mailing, Message, RecipientMailing


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs['class'] = "form-check-input"
            elif isinstance(fild, ImageField):
                fild.widget.attrs['class'] = "form-control-file"
            else:
                fild.widget.attrs['class'] = "form-control"


class RecipientForm(StyleFormMixin, ModelForm):
    class Meta:
        model = RecipientMailing
        fields = "__all__"
        exclude = ['owner']


class MessageForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Message
        fields = "__all__"
        exclude = ['owner']


class MailingForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Mailing
        exclude = [
            "first_sending",
            "end_sending",
            "status",
            "owner"
        ]
