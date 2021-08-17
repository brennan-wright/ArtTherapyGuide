
from datetime import timedelta

import factory
import wagtail_factories
from blog.models import (AuthorIndexPage, AuthorPage, BlogAudience,
                         BlogIndexPage, BlogPage)
from cities_light.models import City, Country, Region, SubRegion
from directive.models import (DirectiveAudience, DirectiveDiagnosis,
                              DirectiveIdentifiedPatient, DirectiveImages,
                              DirectivePage, DirectivePopulation)
from django.contrib.auth import get_user_model
from django.utils import timezone
from education.models import EducationLevel, EducationPage
from home.models import AboutPage, ContactPage, HomePage, PrivacyPolicyPage
from wagtail.core import blocks
from wagtail.core.models import Page
from wagtail.images.models import Image


class CountryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Country
        django_get_or_create = ("code2",)
    name = factory.Faker('city')
    name_ascii = factory.Faker('city')
    slug = factory.Faker('city')
    geoname_id = factory.Faker('numerify', text='##')
    alternate_names = factory.Faker('city')
    code2 = 21
    code3 = factory.Faker('numerify', text='###')
    continent = factory.Faker('numerify', text='##')
    tld = factory.Faker('numerify', text='#####')
    phone = factory.Faker('numerify', text='####################')


class RegionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Region
        django_get_or_create = ("geoname_code",)
    name = factory.Faker('city')
    name_ascii = factory.Faker('city')
    slug = factory.Faker('city')
    geoname_id = factory.Faker('numerify', text='##')
    alternate_names = factory.Faker('city')
    display_name = factory.Faker('city')
    geoname_code = factory.Faker('numerify', text='##')
    country = factory.SubFactory(CountryFactory)


class SubRegionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SubRegion
        django_get_or_create = ("geoname_code",)
    name = factory.Faker('city')
    name_ascii = factory.Faker('city')
    slug = factory.Faker('city')
    geoname_id = factory.Faker('numerify', text='##')
    alternate_names = factory.Faker('city')
    display_name = factory.Faker('city')
    geoname_code = factory.Faker('numerify', text='##')
    region = factory.SubFactory(RegionFactory)
    country = factory.SelfAttribute('region.country')


class CityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = City
        django_get_or_create = ("search_names",)
    name = factory.Faker('city')
    name_ascii = factory.Faker('city')
    slug = factory.Faker('city')
    geoname_id = factory.Faker('numerify', text='##')
    alternate_names = factory.Faker('city')
    display_name = factory.Faker('city')
    search_names = factory.Faker('city')
    latitude = factory.Faker('latitude')
    longitude = factory.Faker('longitude')
    population = factory.Faker('numerify', text='#######')
    feature_code = factory.Faker('numerify', text='##')
    timezone = 'PST'
    country = factory.SelfAttribute('subregion.region.country')
    region = factory.SelfAttribute('subregion.region')
    subregion = factory.SubFactory(
        SubRegionFactory)


class EducationLevelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EducationLevel
    name = factory.Faker('color')


class EducationPageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EducationPage
    remote = factory.Faker('boolean')
    school_name = factory.Faker('company')
    school_url = factory.Faker('uri')
    region = factory.SelfAttribute('city.subregion.region')
    city = factory.SubFactory(CityFactory)

    @factory.post_generation
    def education_level(self, create, extracted, **kwargs):
        if not create:

            return

        if extracted:
            # A list of education_levels were passed in, use them
            for education_level in extracted:
                self.education_level.add(education_level)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Faker('user_name')
    email = factory.Faker('ascii_email')
    password = factory.Faker('password')


class DirectiveDiagnosisFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DirectiveDiagnosis
    name = factory.Faker('city')


class DirectivePopulationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DirectivePopulation
    name = factory.Faker('city')


class DirectiveIdentifiedPatientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DirectiveIdentifiedPatient
    name = factory.Faker('city')


class DirectiveAudienceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DirectiveAudience
    name = factory.Faker('city')


class DirectivePageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DirectivePage
    uuid = factory.Faker('uuid4')
    title = factory.Faker('sentence')
    directive_description = factory.Faker('text', max_nb_chars=20)
    updated = factory.Faker('date_time')

    @factory.post_generation
    def population(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for population in extracted:
                self.population.add(population)

    @factory.post_generation
    def diagnosis(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for diagnosis in extracted:
                self.diagnosis.add(diagnosis)

    @factory.post_generation
    def identified_patient(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for identified_patient in extracted:
                self.identified_patient.add(identified_patient)

    @factory.post_generation
    def audience(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for audience in extracted:
                self.audience.add(audience)


class DirectiveImagesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DirectiveImages
    post = factory.SubFactory(DirectivePageFactory)
    image = factory.django.ImageField()


class PageFactory(factory.django.DjangoModelFactory):
    class Meta:
        abstract = True

    # override the _create method, to establish parent-child relationship between pages
    @classmethod
    def _create(cls, model_class, *args, **kwargs):

        try:
            parent = kwargs.pop('parent')
        except KeyError:
            # no parent, appending page to root
            parent = Page.get_first_root_node()

        page = model_class(*args, **kwargs)
        parent.add_child(instance=page)

        return page


class BlogAudienceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BlogAudience
    name = factory.Faker('city')


class HomePageFactory(PageFactory):
    class Meta:
        model = HomePage

    title = factory.Sequence(lambda n: 'Home page {0}'.format(n))
    first_published_at = factory.Sequence(
        lambda n: timezone.now() - timedelta(days=365-n))


class RichTextBlockFactory(factory.Factory):
    @ classmethod
    def _build(cls, model_class, value=""):
        block = model_class()
        return block.to_python(value)

    @ classmethod
    def _create(cls, model_class, *args, **kwargs):
        return cls._build(model_class, *args, **kwargs)

    class Meta:
        model = blocks.RichTextBlock


class AuthorPageFactory(PageFactory):
    title = factory.Sequence(
        lambda n: 'Author Page number {0}'.format(n))
    first_published_at = factory.Sequence(
        lambda n: timezone.now() - timedelta(days=365-n))
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    body = wagtail_factories.StreamFieldFactory({
        'subheading': wagtail_factories.CharBlockFactory,
        'paragraph': RichTextBlockFactory,
        'image':  wagtail_factories.ImageChooserBlockFactory
    })
    linkedin = factory.Faker('url')
    twitter = factory.Faker('url')
    website = factory.Faker('url')
 #  photo =  TODO Need to add the photo, but have to add a media location for CI first.

    class Meta:
        model = AuthorPage


class AuthorIndexPageFactory(PageFactory):
    title = factory.Sequence(
        lambda n: 'Author Index Page number {0}'.format(n))
    first_published_at = factory.Sequence(
        lambda n: timezone.now() - timedelta(days=365-n))

    class Meta:
        model = AuthorIndexPage


class AboutPageFactory(PageFactory):
    title = factory.Sequence(
        lambda n: 'About Page number {0}'.format(n))
    first_published_at = factory.Sequence(
        lambda n: timezone.now() - timedelta(days=365-n))
    body = factory.Faker('paragraphs')

    class Meta:
        model = AboutPage


class PrivacyPolicyPageFactory(PageFactory):
    title = factory.Sequence(
        lambda n: 'Privacy Policy Page number {0}'.format(n))
    first_published_at = factory.Sequence(
        lambda n: timezone.now() - timedelta(days=365-n))
    body = factory.Faker('paragraphs')

    class Meta:
        model = PrivacyPolicyPage


class ContactPageFactory(PageFactory):
    title = factory.Sequence(
        lambda n: 'Contact Page number {0}'.format(n))
    first_published_at = factory.Sequence(
        lambda n: timezone.now() - timedelta(days=365-n))
    intro = factory.Faker('paragraphs')
    thank_you_text = factory.Faker('paragraphs')

    class Meta:
        model = ContactPage


class BlogIndexPageFactory(PageFactory):
    title = factory.Sequence(
        lambda n: 'Author Index Page number {0}'.format(n))
    first_published_at = factory.Sequence(
        lambda n: timezone.now() - timedelta(days=365-n))

    class Meta:
        model = BlogIndexPage
