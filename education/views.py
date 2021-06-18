from cities_light.models import City
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from wagtail.search.backends import get_search_backend

from .forms import EducationForm
from .models import EducationLevel, EducationPage


def is_valid_queryparam(param):
    return param != '' and param is not None


class ListEducationPage(ListView):
    '''
    The main list view for the listing of all education postings.
    '''
    model = EducationPage
    template_name = 'education/education_index_page.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = EducationPage.objects.order_by('-id')
        s = get_search_backend()

        search_query = self.request.GET.get('search', '')
        education_level = self.request.GET.get('education_level', '')
        region = self.request.GET.get('region', '')
        city = self.request.GET.get('city', '')
        remote = self.request.GET.get('remote', '')
        print(remote)

        if is_valid_queryparam(search_query):
            results = s.search(search_query, qs)
            qs = results.get_queryset()

        if is_valid_queryparam(education_level):
            qs = qs.filter(education_level__name__icontains=education_level)

        if is_valid_queryparam(region):
            qs = qs.filter(region__name__icontains=region)

        if is_valid_queryparam(city):
            qs = qs.filter(city__name__icontains=city)

        if is_valid_queryparam(remote):
            qs = qs.filter(remote=remote)

        return qs

    def get_context_data(self, **kwargs):
        from .forms import EducationPageFilterForm
        context = super().get_context_data(**kwargs)
        context['education_level'] = EducationLevel.objects.all()
        context['form'] = EducationPageFilterForm(self.request.GET)
        context['region'] = EducationPage.objects.all().distinct('region')
        context['city'] = EducationPage.objects.all().distinct('city')
        return context


class ListUserEducationPage(ListView):
    '''
    The main list view for the listing of all education postings.
    '''
    model = EducationPage
    template_name = 'education/user_education_index_page.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = EducationPage.objects.filter(
            posted_by=self.request.user).order_by('-id')
        return qs


class DetailEducationPage(DetailView):
    '''
    Main detail veiw for education postings.
    '''
    # specify the model to use
    model = EducationPage
    slug_url_kwarg = 'uuid'
    slug_field = 'uuid'
    context_object_name = 'page'
    template_name = 'education/education_page.html'


def thanks(request, uuid):
    '''
    This shows the thank you page after creating a education posting.
    '''
    docrequest = EducationPage.objects.get(uuid=uuid)

    return render(request, 'education/educationpage_thankyou.html', {'docrequest': docrequest})


class CreateEducationPage(LoginRequiredMixin, CreateView):
    '''
    This is the create view for creating a new education posting. Redirects to the thank you page after completing a posting.
    '''
    form_class = EducationForm
    model = EducationPage

    template_name = 'education/educationpage_form.html'

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        form.instance.created_date = timezone.now()
        return super(CreateEducationPage, self).form_valid(form)

    def get_success_url(self):
        return reverse('thanks_education_post', kwargs={'uuid': self.object.uuid})


class EditEducationPage(LoginRequiredMixin, UpdateView):
    '''
    This is the view for editing an already existing education posting. Redirects to the Thank you page when submitted.
    '''
    form_class = EducationForm
    model = EducationPage
    template_name = 'education/educationpage_form.html'
    slug_url_kwarg = 'uuid'
    slug_field = 'uuid'
    context_object_name = 'page'

    def get_queryset(self):
        return EducationPage.objects.filter(posted_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.date_updated = timezone.now()
        post.save()
        return super(EditEducationPage, self).form_valid(form)

    def get_success_url(self):
        return reverse('thanks_education_post', kwargs={'uuid': self.object.uuid})


class DeleteEducationPage(LoginRequiredMixin, DeleteView):
    '''
    This is the view that deleted a post. Does not actually render a page.
    '''
    model = EducationPage
    success_url = "/"
    slug_url_kwarg = 'uuid'
    slug_field = 'uuid'

    def get_queryset(self):
        return EducationPage.objects.filter(posted_by=self.request.user)


def load_cities(request):
    region_id = request.GET.get('region')
    cities = City.objects.filter(region_id=region_id).order_by('name')
    return render(request, 'education/cities_dropdown_list_options.html', {'cities': cities})
