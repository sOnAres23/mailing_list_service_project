from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.urls import reverse_lazy

from mailing.forms import StyleFormMixin
from users.models import User


class CustomUserCreationForm(StyleFormMixin, UserCreationForm):
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
        fields = (
            "first_name",
            "last_name",
            "email",
            "password",
            "phone_number",
            "country",
            "is_active",
            "is_superuser",
            "is_staff",
            "avatar",
        )
        success_url = reverse_lazy("users:users")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        phone_number = self.fields["phone_number"].widget

        self.fields["password"].widget = forms.HiddenInput()
        phone_number.attrs["class"] = "form-control bfh-phone"
        phone_number.attrs["data-format"] = "+7 (ddd) ddd-dd-dd"

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Пользователь с таким Email уже существует.")

        return email


# class PasswordRecoveryForm(StyleFormMixin, forms.Form):
#     email = forms.EmailField(label="Укажите Email")
#
#     def clean_email(self):
#         """
#         Проверка email на уникальность
#         """
#         email = self.cleaned_data.get("email")
#         if not User.objects.filter(email=email).exists():
#             raise forms.ValidationError("Такого email нет в системе")
#         return email
