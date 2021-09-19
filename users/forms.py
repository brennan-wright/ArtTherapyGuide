from allauth.account.forms import SignupForm
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from django import forms
from django.contrib.auth import get_user_model


class CustomSignupForm(SignupForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3)
    field_order = ['email', 'username', 'password1', 'password2', 'captcha',
                   ]

    class Meta:
        model = get_user_model()

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.fields['captcha'].label = ""


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
