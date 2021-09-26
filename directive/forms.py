from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from .models import (DirectiveInstruction, DirectiveMaterial,
                     DirectiveObjective, DirectivePage)


class DirectivePageFilterForm(forms.Form):
    '''
    This is only used to render the education index page's search field.
    '''
    search = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
                             'placeholder': 'Search'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search'].label = False


class DirectiveObjectiveForm(ModelForm):
    '''
    This form is used by both the create view and the edit view for directive posts.
    '''
    class Meta:
        model = DirectiveObjective
        fields = ['objective', ]


class DirectiveMaterialForm(ModelForm):
    '''
    This form is used by both the create view and the edit view for directive posts.
    '''
    class Meta:
        model = DirectiveMaterial
        fields = ['material', ]


class DirectiveInstructionForm(ModelForm):
    '''
    This form is used by both the create view and the edit view for directive posts.
    '''
    class Meta:
        model = DirectiveInstruction
        fields = ['instruction', ]


DirectiveObjectiveFormSet = inlineformset_factory(
    DirectivePage, DirectiveObjective, form=DirectiveObjectiveForm,
    extra=1, can_delete=True, min_num=1, validate_min=True
)

DirectiveMaterialFormSet = inlineformset_factory(
    DirectivePage, DirectiveMaterial, form=DirectiveMaterialForm,
    extra=1, can_delete=True,  min_num=1, validate_min=True
)

DirectiveInstructionFormSet = inlineformset_factory(
    DirectivePage, DirectiveInstruction, form=DirectiveInstructionForm,
    extra=1, can_delete=True, min_num=1, validate_min=True
)
