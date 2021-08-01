from allauth.account.forms import SignupForm
from captcha.fields import ReCaptchaField
from django import forms
from django.contrib.auth import get_user_model


class MyCustomSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=150, widget=forms.TextInput(attrs={'placeholder': 'First Name'}), label='First Name', required=True)
    last_name = forms.CharField(
        max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}), label='Last Name', required=True)
    captcha = ReCaptchaField()
    field_order = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'captcha',
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
