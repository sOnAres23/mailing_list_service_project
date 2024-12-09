from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from mailing.forms import StyleFormMixin
from users.models import User


class CustomUserCreationForm(StyleFormMixin, UserCreationForm):
    username = forms.CharField(max_length=50, required=False, help_text="Можете не заполнять")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone_number',
                  'country', 'password1', 'password2', 'avatar')
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }


class UserUpdateForm(StyleFormMixin, ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone_number", "country", "avatar")

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Пользователь с таким Email уже существует.")

        return email


class PasswordRecoveryForm(StyleFormMixin, forms.Form):
    email = forms.EmailField(label="Укажите Email")

    def clean_email(self):
        """Проверка email на уникальность"""
        email = self.cleaned_data.get("email")
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Такого email нет в системе")
        return email
