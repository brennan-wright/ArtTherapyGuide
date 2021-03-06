import re

from allauth.account.forms import SignupForm
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.forms.models import ModelForm


class CustomSignupForm(SignupForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    if getattr(settings, "DEBUG", False):
        captcha.clean = lambda x: True
    field_order = ['email', 'username', 'password1', 'password2', 'captcha',
                   ]

    class Meta:
        model = get_user_model()

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.fields['captcha'].label = ""

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username__iexact=username).exists():
            self.add_error(
                "username", "A user with this username already exists.")

        if not re.match(r'[a-zA-Z0-9_@#-]+', username):
            self.add_error(
                "username", "Invalid username")

        return username


class UserDeactivateForm(forms.Form):
    """
    Simple form that provides a checkbox that signals deactivation.
    """
    deactivate = forms.BooleanField(required=True)


class UserDeleteForm(forms.Form):
    """
    Simple form that provides a checkbox that signals deletion.
    """
    delete = forms.BooleanField(required=True)


class UserChangeUsernameForm(ModelForm):
    """
    Form to allow users to change their username.
    """
    class Meta:
        model = get_user_model()
        fields = ['username', ]
