from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm
)
from django import forms
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class AuthenticationAjaxForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Password'})