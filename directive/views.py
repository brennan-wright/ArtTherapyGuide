from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import DeleteView, UpdateView

from .forms import (DirectiveInstructionFormSet, DirectiveMaterialFormSet,
                    DirectiveObjectiveFormSet)
from .models import DirectiveDiagnosis, DirectivePage, DirectivePopulation


def is_valid_queryparam(param):
    return param != '' and param is not None


class ListDirectivePage(ListView):
    '''
    The main list view for the listing of all directive postings.
    '''
    model = DirectivePage
    template_name = 'directive/directive_index_page.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self, *args, **kwargs):
        qs = DirectivePage.objects.order_by('-id')
        search = self.request.GET.get('search', '')
        population = self.request.GET.get('population', '')
        diagnosis = self.request.GET.get('diagnosis', '')

        if is_valid_queryparam(search):
            qs = qs.filter(title__icontains=search)

        if is_valid_queryparam(population):
            qs = qs.filter(population__name__icontains=population)

        if is_valid_queryparam(diagnosis):
            qs = qs.filter(diagnosis__name__icontains=diagnosis)

        return qs

    def get_context_data(self, **kwargs):
        from .forms import DirectivePageFilterForm
        context = super().get_context_data(**kwargs)
        context['population'] = DirectivePopulation.objects.all()
        context['diagnosis'] = DirectiveDiagnosis.objects.all()
        context['form'] = DirectivePageFilterForm(self.request.GET)
        return context


class DetailDirectivePage(DetailView):
    '''
    Main detail veiw for directive postings.
    '''
    model = DirectivePage
    slug_url_kwarg = 'uuid'
    slug_field = 'uuid'
    context_object_name = 'page'
    template_name = 'directive/directive_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ThanksPage(TemplateView):
    '''
    Page to redirect to after submitting a post or edit.
    '''
    template_name = 'directive/directivepage_thankyou.html'

    def get_context_data(self, uuid, **kwargs):
        context = super(ThanksPage, self).get_context_data(**kwargs)
        context['docrequest'] = DirectivePage.objects.filter(
            uuid=uuid).first()  # TODO this is a weird way to get that item.
        return context


class CreateDirectivePage(LoginRequiredMixin, CreateView):
    '''
    This is the create view for creating a new directive posting. Redirects to the thank you page after completing a posting.
    '''
    fields = ['title', 'intro', 'population', 'diagnosis', 'discussion']
    model = DirectivePage
    template_name = 'directive/directivepage_form.html'

    def get_context_data(self, **kwargs):
        data = super(CreateDirectivePage,
                     self).get_context_data(**kwargs)
        if self.request.POST:
            data['objectiveformset'] = DirectiveObjectiveFormSet(
                self.request.POST)
            data['materialformset'] = DirectiveMaterialFormSet(
                self.request.POST)
            data['instructionformset'] = DirectiveInstructionFormSet(
                self.request.POST)
        else:
            data['objectiveformset'] = DirectiveObjectiveFormSet()
            data['materialformset'] = DirectiveMaterialFormSet()
            data['instructionformset'] = DirectiveInstructionFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        directiveobjective = context['objectiveformset']
        directivematerial = context['materialformset']
        directiveinstruction = context['instructionformset']
        with transaction.atomic():
            form.instance.posted_by = self.request.user
            self.object = form.save()
            if directiveobjective.is_valid():
                directiveobjective.instance = self.object
                directiveobjective.save()
            if directivematerial.is_valid():
                directivematerial.instance = self.object
                directivematerial.save()
            if directiveinstruction.is_valid():
                directiveinstruction.instance = self.object
                directiveinstruction.save()
            else:
                return self.form_invalid(form)
        return super(CreateDirectivePage, self).form_valid(form)

    def get_success_url(self):
        return reverse('thanks_directive_post', kwargs={'uuid': self.object.uuid})


class EditDirectivePage(LoginRequiredMixin, UpdateView):
    '''
    This is the create view for creating a new directive posting. Redirects to the thank you page after completing a posting.
    '''
    fields = ['title', 'intro', 'population', 'diagnosis']
    model = DirectivePage
    slug_url_kwarg = 'uuid'
    slug_field = 'uuid'
    template_name = 'directive/directivepage_form.html'

    def get_context_data(self, **kwargs):

        context = super(EditDirectivePage,
                        self).get_context_data(**kwargs)
        if self.request.POST:
            context['objectiveformset'] = DirectiveObjectiveFormSet(
                self.request.POST, instance=self.object)
            context['materialformset'] = DirectiveMaterialFormSet(
                self.request.POST, instance=self.object)
            context['instructionformset'] = DirectiveInstructionFormSet(
                self.request.POST, instance=self.object)
        else:
            context['objectiveformset'] = DirectiveObjectiveFormSet(
                instance=self.object)
            context['materialformset'] = DirectiveMaterialFormSet(
                instance=self.object)
            context['instructionformset'] = DirectiveInstructionFormSet(
                instance=self.object)

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        directiveobjective = context['objectiveformset']
        directivematerial = context['materialformset']
        directiveinstruction = context['instructionformset']
        with transaction.atomic():
            self.object = form.save()
            if directiveobjective.is_valid():
                directiveobjective.instance = self.object
                directiveobjective.save()
            if directivematerial.is_valid():
                directivematerial.instance = self.object
                directivematerial.save()
            if directiveinstruction.is_valid():
                directiveinstruction.instance = self.object
                directiveinstruction.save()
        return super(EditDirectivePage, self).form_valid(form)

    def get_success_url(self):
        return reverse('thanks_directive_post', kwargs={'uuid': self.object.uuid})


class DeleteDirectivePage(LoginRequiredMixin, DeleteView):
    '''
    This is the view that deleted a post. Does not actually render a page.
    '''
    model = DirectivePage
    success_url = "/"
    slug_url_kwarg = 'uuid'
    slug_field = 'uuid'

    def get_queryset(self):
        return DirectivePage.objects.filter(posted_by=self.request.user)


class ListUserDirectivePage(ListView):
    '''
    The main list view for the listing of all directive postings.
    '''
    model = DirectivePage
    template_name = 'directive/user_directive_index_page.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = DirectivePage.objects.filter(
            posted_by=self.request.user).order_by('-id')
        return qs
