# dwitter/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Dweet, Mensagens


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


class RespostaForm(forms.ModelForm):
    texto = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Escreva uma msg...",
                "class": "textarea is-success is-medium",
            }
        ),
        label="",
    )


    class Meta:
        model = Mensagens
        exclude = ("user", )

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)


class CustomUserPasswordChangeForm(PasswordChangeForm):
    class Meta(PasswordChangeForm):
        model = User
