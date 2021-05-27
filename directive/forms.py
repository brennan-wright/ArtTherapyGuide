from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.forms.widgets import SelectMultiple, TextInput
from tinymce.widgets import TinyMCE

from .models import DirectiveImages, DirectivePage


def file_size(value):  # add this to some file where you can import it from
    limit = 1000000 * 10
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 10 MB.')


class DirectivePageFilterForm(forms.Form):
    '''
    This is only used to render the education index page's search field.
    '''

    search = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
                             'placeholder': 'Search'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search'].label = False


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image', validators=[file_size])

    class Meta:
        model = DirectiveImages
        fields = ('image', )


class DirectiveForm(ModelForm):
    '''
    This form is used by both the create view and the edit view for education posts.
    '''

    class Meta:
        model = DirectivePage
        fields = ['title', 'population', 'diagnosis',
                  'audience', 'directive_description']
        widgets = {
            'title': TextInput(attrs={'placeholder': 'Title or Name of Directive', 'class': 'form-control'}),
            'population': SelectMultiple(attrs={'class': 'form-control'}),
            'diagnosis': SelectMultiple(attrs={'class': 'form-control'}),
            'audience': SelectMultiple(attrs={'class': 'form-control'}),
            'directive_description': TinyMCE(attrs={'cols': 80, 'rows': 30}),
        }


DirectiveImageFormSet = inlineformset_factory(
    DirectivePage, DirectiveImages, form=ImageForm,
    fields=['image', ], extra=3, max_num=3, can_delete=True
)
