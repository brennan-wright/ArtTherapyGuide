from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django.views.generic.base import TemplateView

from .forms import DirectiveForm
from .models import (DirectiveAudience, DirectiveDiagnosis,
                     DirectiveIdentifiedPatient, DirectivePage,
                     DirectivePopulation)


def is_valid_queryparam(param):
    return param != '' and param is not None


class ListDirectivePage(ListView):
    '''
    The main list view for the listing of all directive postings.
    '''
    model = DirectivePage
    template_name = 'directive/directive_index_page.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = DirectivePage.objects.order_by('-id')

        audience = self.request.GET.get('audience', '')
        population = self.request.GET.get('population', '')
        diagnosis = self.request.GET.get('diagnosis', '')
        identified_patient = self.request.GET.get('identified_patient', '')

        if is_valid_queryparam(audience):
            qs = qs.filter(audience__name__icontains=audience)

        if is_valid_queryparam(population):
            qs = qs.filter(population__name__icontains=population)

        if is_valid_queryparam(diagnosis):
            qs = qs.filter(diagnosis__name__icontains=diagnosis)

        if is_valid_queryparam(identified_patient):
            qs = qs.filter(
                identified_patient__name__icontains=identified_patient)

        return qs

    def get_context_data(self, **kwargs):
        from .forms import DirectivePageFilterForm
        context = super().get_context_data(**kwargs)
        context['audience'] = DirectiveAudience.objects.all()
        context['population'] = DirectivePopulation.objects.all()
        context['diagnosis'] = DirectiveDiagnosis.objects.all()
        context['identified_patient'] = DirectiveIdentifiedPatient.objects.all()
        context['form'] = DirectivePageFilterForm(self.request.GET)
        return context


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
    form_class = DirectiveForm
    model = DirectivePage
    template_name = 'directive/directivepage_form.html'

    def get_success_url(self):
        return reverse('thanks_directive_post', kwargs={'uuid': self.object.uuid})


class EditDirectivePage(LoginRequiredMixin, UpdateView):
    '''
    This is the view for editing an already existing directive posting. Redirects to the Thank you page when submitted.
    '''
    form_class = DirectiveForm
    model = DirectivePage
    template_name = 'directive/directivepage_form.html'
    slug_url_kwarg = 'uuid'
    slug_field = 'uuid'
    context_object_name = 'page'

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
