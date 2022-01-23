from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import (SearchQuery, SearchRank,
                                            SearchVector)
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import DeleteView, UpdateView

from .forms import (DirectiveInstructionFormSet, DirectiveMaterialFormSet,
                    DirectiveObjectiveFormSet, DirectivePageForm)
from .models import (DirectiveDiagnosis, DirectiveImage, DirectivePage,
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
    paginate_by = 15

    def get_queryset(self, *args, **kwargs):
        qs = DirectivePage.objects.order_by('-id')
        search = self.request.GET.get('search', '')
        population = self.request.GET.get('population', '')
        diagnosis = self.request.GET.get('diagnosis', '')

        if is_valid_queryparam(population):
            qs = qs.filter(population__name__icontains=population)

        if is_valid_queryparam(diagnosis):
            qs = qs.filter(diagnosis__name__icontains=diagnosis)

        if is_valid_queryparam(search):
            vector = SearchVector('title', 'intro', 'population__name', 'diagnosis__name', 'discussion', 'instructions__instruction', 'materials__material',
                                  'objectives__objective')
            query = SearchQuery(search)
            rank = SearchRank(vector, query)

            qs = qs.annotate(search=vector, rank=rank).filter(
                search=query).order_by('id', '-rank').distinct('id')

            # TODO: If performance becomes an issue, add the search vector field to the model, and then search off that. Needs a cron job or something to update so postponing until it is really slow.
            # http://blog.lotech.org/postgres-full-text-search-with-django.html

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
    Main detail view for directive postings.
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


@login_required
def create_directive_page(request):

    form = DirectivePageForm()
    objectiveformset = DirectiveObjectiveFormSet()
    materialformset = DirectiveMaterialFormSet()
    instructionformset = DirectiveInstructionFormSet()

    if request.method == 'POST':
        form = DirectivePageForm(request.POST)
        objectiveformset = DirectiveObjectiveFormSet(request.POST)
        materialformset = DirectiveMaterialFormSet(request.POST)
        instructionformset = DirectiveInstructionFormSet(request.POST)
        files = [request.FILES.get('file[%d]' % i)
                 for i in range(0, len(request.FILES))]
        form.instance.posted_by = request.user
        if form.is_valid() and objectiveformset.is_valid() and materialformset.is_valid() and instructionformset.is_valid():
            with transaction.atomic():
                form = form.save()

                objectiveformset.instance = form
                objectiveformset.save()

                materialformset.instance = form
                materialformset.save()

                instructionformset.instance = form
                instructionformset.save()

                for image in files:
                    print('fart')
                    photo = DirectiveImage(
                        image=image, directive=form)
                    photo.save()

            link = reverse('home')

            response = {'url': link}

            return JsonResponse(response)

    return render(request, 'directive/directivepage_form.html', {
        'form': form,
        'objectiveformset': objectiveformset,
        'materialformset': materialformset,
        'instructionformset': instructionformset})


class EditDirectivePage(LoginRequiredMixin, UpdateView):
    '''
    This is the create view for creating a new directive posting. Redirects to the thank you page after completing a posting.
    '''
    fields = ['title', 'intro', 'population', 'diagnosis', 'discussion']
    model = DirectivePage
    slug_url_kwarg = 'uuid'
    slug_field = 'uuid'
    template_name = 'directive/directivepage_form.html'
    context_object_name = 'page'

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

    @transaction.atomic
    def form_valid(self, form):
        context = self.get_context_data()
        directiveobjective = context['objectiveformset']
        directivematerial = context['materialformset']
        directiveinstruction = context['instructionformset']

        self.object = form.save()
        if directiveobjective.is_valid() and directivematerial.is_valid() and directiveinstruction.is_valid():
            directiveobjective.instance = self.object
            directiveobjective.save()

            directivematerial.instance = self.object
            directivematerial.save()

            directiveinstruction.instance = self.object
            directiveinstruction.save()

        else:
            return self.form_invalid(form)
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
    paginate_by = 15

    def get_queryset(self, *args, **kwargs):
        qs = DirectivePage.objects.filter(
            posted_by=self.request.user).order_by('-id')
        return qs
