from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory, modelformset_factory

from .models import DirectiveObjective, DirectivePage


class DirectivePageFilterForm(forms.Form):
    '''
    This is only used to render the education index page's search field.
    '''
    search = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
                             'placeholder': 'Search'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search'].label = False


class DirectiveForm(ModelForm):
    '''
    This form is used by both the create view and the edit view for education posts.
    '''
    class Meta:
        model = DirectivePage
        fields = ['title', 'intro', 'population', 'diagnosis']


class DirectiveObjectiveForm(ModelForm):
    '''
    This form is used by both the create view and the edit view for education posts.
    '''
    class Meta:
        model = DirectiveObjective
        fields = ['objective', ]


DirectiveObjectiveFormSet = inlineformset_factory(
    DirectivePage, DirectiveObjective, form=DirectiveObjectiveForm,
    extra=2, can_delete=True
)
