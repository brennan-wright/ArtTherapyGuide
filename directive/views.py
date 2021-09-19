from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.base import TemplateView

from .forms import DirectiveForm, DirectiveObjectiveFormSet
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
    fields = ['title', 'intro', 'population', 'diagnosis']
    model = DirectivePage
    template_name = 'directive/directivepage_form.html'

    def get_context_data(self, **kwargs):
        data = super(CreateDirectivePage,
                     self).get_context_data(**kwargs)
        if self.request.POST:
            data['directiveobjective'] = DirectiveObjectiveFormSet(
                self.request.POST)
        else:
            data['directiveobjective'] = DirectiveObjectiveFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        directiveobjective = context['directiveobjective']
        with transaction.atomic():
            self.object = form.save()

            if directiveobjective.is_valid():
                directiveobjective.instance = self.object
                directiveobjective.save()
        return super(CreateDirectivePage, self).form_valid(form)

    def get_success_url(self):
        return reverse('thanks_directive_post', kwargs={'uuid': self.object.uuid})
