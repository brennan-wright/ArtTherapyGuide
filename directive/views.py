from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import (SearchQuery, SearchRank,
                                            SearchVector)
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import DeleteView

from .forms import (DirectiveImageFormSet, DirectiveInstructionFormSet,
                    DirectiveMaterialFormSet, DirectiveObjectiveFormSet,
                    DirectivePageForm)
from .models import DirectiveTheme, DirectivePage, DirectivePopulation


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
        theme = self.request.GET.get('theme', '')

        if is_valid_queryparam(population):
            qs = qs.filter(population__name__icontains=population)

        if is_valid_queryparam(theme):
            qs = qs.filter(theme__name__icontains=theme)

        if is_valid_queryparam(search):
            vector = SearchVector('title', 'intro', 'population__name', 'theme__name', 'discussion', 'instructions__instruction', 'materials__material',
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
        context['theme'] = DirectiveTheme.objects.all()
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
    imageformset = DirectiveImageFormSet()

    if request.method == 'POST':
        form = DirectivePageForm(request.POST)
        objectiveformset = DirectiveObjectiveFormSet(request.POST)
        materialformset = DirectiveMaterialFormSet(request.POST)
        instructionformset = DirectiveInstructionFormSet(request.POST)
        imageformset = DirectiveImageFormSet(request.POST, request.FILES)

        form.instance.posted_by = request.user
        if form.is_valid() and objectiveformset.is_valid() and materialformset.is_valid() and instructionformset.is_valid() and imageformset.is_valid():
            with transaction.atomic():
                form = form.save()

                objectiveformset.instance = form
                objectiveformset.save()

                materialformset.instance = form
                materialformset.save()

                instructionformset.instance = form
                instructionformset.save()

                imageformset.instance = form
                imageformset.save()

            return redirect("thanks_directive_post", uuid=form.uuid)

    return render(request, 'directive/directivepage_form.html', {
        'form': form,
        'objectiveformset': objectiveformset,
        'materialformset': materialformset,
        'instructionformset': instructionformset,
        'imageformset': imageformset,
    })


@login_required
def edit_directive_page(request, uuid):

    obj = get_object_or_404(DirectivePage, uuid=uuid)

    form = DirectivePageForm(request.POST or None, instance=obj)
    objectiveformset = DirectiveObjectiveFormSet(
        request.POST or None, instance=obj)
    materialformset = DirectiveMaterialFormSet(
        request.POST or None, instance=obj)
    instructionformset = DirectiveInstructionFormSet(
        request.POST or None, instance=obj)
    imageformset = DirectiveImageFormSet(request.POST or None, instance=obj)

    if request.method == 'POST':
        form = DirectivePageForm(request.POST, instance=obj)
        objectiveformset = DirectiveObjectiveFormSet(
            request.POST, instance=obj)
        materialformset = DirectiveMaterialFormSet(request.POST, instance=obj)
        instructionformset = DirectiveInstructionFormSet(
            request.POST, instance=obj)
        imageformset = DirectiveImageFormSet(
            request.POST, request.FILES, instance=obj)

        form.instance.posted_by = request.user
        if form.is_valid() and objectiveformset.is_valid() and materialformset.is_valid() and instructionformset.is_valid() and imageformset.is_valid():
            with transaction.atomic():
                form = form.save()

                objectiveformset.instance = form
                objectiveformset.save()

                materialformset.instance = form
                materialformset.save()

                instructionformset.instance = form
                instructionformset.save()

                imageformset.instance = form
                imageformset.save()

            return redirect("thanks_directive_post", uuid=obj.uuid)

    return render(request, 'directive/directivepage_form.html', {
        'page': obj,
        'form': form,
        'objectiveformset': objectiveformset,
        'materialformset': materialformset,
        'instructionformset': instructionformset,
        'imageformset': imageformset,
    })


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
