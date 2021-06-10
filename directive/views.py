from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django.views.generic.base import TemplateView
from wagtail.search.backends import get_search_backend

from .forms import DirectiveForm, DirectiveImageFormSet
from .models import (DirectiveAudience, DirectiveDiagnosis, DirectiveImages,
                     DirectivePage, DirectivePopulation)


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
        s = get_search_backend()

        search_query = self.request.GET.get('search', '')
        audience = self.request.GET.get('audience', '')
        population = self.request.GET.get('population', '')
        diagnosis = self.request.GET.get('diagnosis', '')
        datemax = self.request.GET.get('date_max', '')
        datemin = self.request.GET.get('date_min', '')

        if is_valid_queryparam(search_query):
            results = s.search(search_query, qs)
            qs = results.get_queryset()

        if is_valid_queryparam(audience):
            qs = qs.filter(audience__name__icontains=audience)

        if is_valid_queryparam(population):
            qs = qs.filter(population__name__icontains=population)

        if is_valid_queryparam(diagnosis):
            qs = qs.filter(diagnosis__name__icontains=diagnosis)

        if is_valid_queryparam(datemin):
            qs = qs.filter(created__gte=datemin)

        if is_valid_queryparam(datemax):
            qs = qs.filter(created__lt=datemax)

        return qs

    def get_context_data(self, **kwargs):
        from .forms import DirectivePageFilterForm
        context = super().get_context_data(**kwargs)
        context['audience'] = DirectiveAudience.objects.all()
        context['population'] = DirectivePopulation.objects.all()
        context['diagnosis'] = DirectiveDiagnosis.objects.all()
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
    # specify the model to use
    model = DirectivePage
    slug_url_kwarg = 'uuid'
    slug_field = 'uuid'
    context_object_name = 'page'
    template_name = 'directive/directive_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = DirectiveImages.objects.filter(post=self.object.id)
        return context


class ThanksPage(TemplateView):
    template_name = 'directive/directivepage_thankyou.html'

    def get_context_data(self, uuid, **kwargs):
        context = super(ThanksPage, self).get_context_data(**kwargs)
        context['docrequest'] = DirectivePage.objects.filter(
            uuid=uuid).first()
        return context


class CreateDirectivePage(LoginRequiredMixin, CreateView):
    '''
    This is the create view for creating a new directive posting. Redirects to the thank you page after completing a posting.
    '''
    form_class = DirectiveForm
    model = DirectivePage
    template_name = 'directive/directivepage_form.html'

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        image_form = DirectiveImageFormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  image_form=image_form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        image_form = DirectiveImageFormSet(
            self.request.POST, files=self.request.FILES)
        if (form.is_valid() and image_form.is_valid()):
            return self.form_valid(form, image_form)
        else:
            return self.form_invalid(form, image_form)

    def form_valid(self, form, image_form):
        """
        Called if all forms are valid. Creates a Recipe instance along with
        associated Ingredients and Instructions and then redirects to a
        success page.
        """
        form.instance.posted_by = self.request.user
        self.object = form.save()

        image_form.instance = self.object
        image_form.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, image_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  image_form=image_form))

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

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        image_form = DirectiveImageFormSet(instance=self.object)
        return self.render_to_response(
            self.get_context_data(form=form,
                                  image_form=image_form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        image_form = DirectiveImageFormSet(
            self.request.POST, files=self.request.FILES, instance=self.object)
        if (form.is_valid() and image_form.is_valid()):
            return self.form_valid(form, image_form)
        else:
            return self.form_invalid(form, image_form)

    def form_valid(self, form, image_form):
        """
        Called if all forms are valid. Creates a Recipe instance along with
        associated Ingredients and Instructions and then redirects to a
        success page.
        """
        self.object = form.save()
        image_form.instance = self.object
        image_form.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, image_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  image_form=image_form))

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
