# dwitter/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Dweet


class DweetForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Escreva uma msg...",
                "class": "textarea is-success is-small",
            }
        ),
        label="",
    )

    class Meta:
        model = Dweet
        exclude = ("user", )


class ConviteAmigoForm(forms.Form):
    nome = forms.CharField(label='Nome', max_length=100,
                           required=True
                           )
    email = forms.EmailField(label="Endereço de e-mail",
                             widget=forms.widgets.EmailInput(attrs={"class": "email", "placeholder": "E-mail",
                                                                    "icon": "is-small is-left fa-solid fa-envelope",
                                                                    }
                                                             )
                             )


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)


class CustomUserPasswordChangeForm(PasswordChangeForm):
    class Meta(PasswordChangeForm):
        model = User
