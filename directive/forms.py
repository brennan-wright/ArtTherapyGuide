from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from .models import (DirectiveImage, DirectiveInstruction, DirectiveMaterial,
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


class DirectivePageForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'required': True, 'class': 'form-control'})
        self.fields['intro'].widget.attrs.update(
            {'required': True, 'class': 'form-control'})
        self.fields['population'].widget.attrs.update(
            {'required': True, 'class': 'form-control'})
        self.fields['theme'].widget.attrs.update(
            {'required': True, 'class': 'form-control'})
        self.fields['discussion'].widget.attrs.update(
            {'required': True, 'class': 'form-control'})

    class Meta:
        model = DirectivePage
        fields = ['title', 'intro', 'population', 'theme', 'discussion']


class DirectiveObjectiveForm(ModelForm):
    '''
    This form is used by both the create view and the edit view for directive posts.
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['objective'].widget.attrs.update(
            {'rows': '1', 'required': True, 'class': 'form-control'})

    class Meta:
        model = DirectiveObjective
        fields = ['objective', ]


class DirectiveMaterialForm(ModelForm):
    '''
    This form is used by both the create view and the edit view for directive posts.
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['material'].widget.attrs.update(
            {'rows': '1', 'required': True, 'class': 'form-control'})

    class Meta:
        model = DirectiveMaterial
        fields = ['material', ]


class DirectiveInstructionForm(ModelForm):
    '''
    This form is used by both the create view and the edit view for directive posts.
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['instruction'].widget.attrs.update(
            {'rows': '1', 'required': True, 'class': 'form-control'})

    class Meta:
        model = DirectiveInstruction
        fields = ['instruction', ]


class DirectiveImageForm(ModelForm):
    '''
    This form is used by both the create view and the edit view for directive posts.
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update(
            {'class': 'form-control'})

    class Meta:
        model = DirectiveImage
        fields = ['image', ]


DirectiveImageFormSet = inlineformset_factory(
    DirectivePage, DirectiveImage, form=DirectiveImageForm,
    extra=3, can_delete_extra=True, can_delete=True, max_num=3, validate_max=True
)

DirectiveObjectiveFormSet = inlineformset_factory(
    DirectivePage, DirectiveObjective, form=DirectiveObjectiveForm,
    extra=0, can_delete=True, min_num=1, max_num=30, validate_max=True, validate_min=True
)

DirectiveMaterialFormSet = inlineformset_factory(
    DirectivePage, DirectiveMaterial, form=DirectiveMaterialForm,
    extra=0, can_delete=True,  min_num=1, max_num=30, validate_max=True, validate_min=True
)

DirectiveInstructionFormSet = inlineformset_factory(
    DirectivePage, DirectiveInstruction, form=DirectiveInstructionForm,
    extra=0, can_delete=True, min_num=1, max_num=30, validate_max=True, validate_min=True
)
