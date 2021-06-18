
from captcha.fields import ReCaptchaField
from cities_light.models import City
from django import forms
from django.forms import ModelForm, Select, TextInput, URLInput
from django.forms.widgets import CheckboxInput, SelectMultiple

from .models import EducationPage


class EducationPageFilterForm(forms.Form):
    '''
    This is only used to render the education index page's search field.
    '''

    search = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
                             'placeholder': 'Search'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search'].label = False


class EducationForm(ModelForm):
    '''
    This form is used by both the create view and the edit view for education posts.
    '''
    captcha = ReCaptchaField()

    class Meta:
        model = EducationPage
        fields = ['school_name', 'education_level', 'remote', 'region', 'city',
                  'school_url']
        widgets = {
            'school_name': TextInput(attrs={'placeholder': 'School Name', 'class': 'form-control'}),
            'education_level': SelectMultiple(attrs={'placeholder': 'Education level', 'class': 'form-control'}),
            'region': Select(attrs={'placeholder': 'region', 'class': 'form-control'}),
            'city': Select(attrs={'placeholder': 'City', 'class': 'form-control'}),
            'remote': CheckboxInput(attrs={'placeholder': 'Remote?', 'class': 'form-check'}),
            'school_url': URLInput(attrs={'placeholder': 'School URL', 'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.fields['captcha'].label = ""

        self.fields['city'].queryset = City.objects.none()

        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['city'].queryset = City.objects.filter(
                    region_id=region_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.region.city_set.order_by(
                'name')
