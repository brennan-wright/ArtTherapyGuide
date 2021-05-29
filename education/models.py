import uuid

import bleach
from cities_light.models import City, Region
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from djrichtextfield.models import RichTextField
from tinymce import models as tinymce_models
from wagtail.search import index


def clean_html(html):
    authorized_tags = [
        'p', 'h3', 'strong', 'em',
        'i', 'b'
    ]
    authorized_attributes = {}

    return bleach.clean(
        html, authorized_tags, authorized_attributes, strip=True)


class EducationRemote(models.Model):
    name = models.CharField(max_length=250, verbose_name="Remote Work Name")

    def __str__(self):
        return self.name


class EducationLevel(models.Model):
    name = models.CharField(
        max_length=250, verbose_name="Education Level Name")

    def __str__(self):
        return self.name


class EducationAudience(models.Model):
    name = models.CharField(max_length=250, verbose_name="Audience Name")

    def __str__(self):
        return self.name


class EducationPage(index.Indexed, models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        verbose_name="Random string for url",
    )
    school_name = models.CharField(
        max_length=250,
        verbose_name="School or Company Name",
    )
    degree_offered = models.CharField(
        max_length=250,
        verbose_name="Degree or Certificate Name",
    )
    education_description_new = tinymce_models.HTMLField(null=True)
    education_level = models.ManyToManyField(
        EducationLevel, related_name='educationposts',
        verbose_name="What is the level of education that will be acheived after attending?")
    school_url = models.URLField(
        max_length=250,
        blank=True,
        verbose_name="URL to School or Company",
    )
    region = models.ForeignKey(
        Region, null=True, on_delete=models.SET_NULL, verbose_name="Region",)
    city = models.ForeignKey(
        City, null=True, on_delete=models.SET_NULL, verbose_name="City",)
    audience = models.ManyToManyField(
        EducationAudience, related_name='educationposts',
        verbose_name="Who is the target audience?")
    remote = models.ManyToManyField(
        EducationRemote, related_name='educationposts',
        verbose_name="Is the Class or Program Remote?")
    created = models.DateTimeField(null=True, editable=False)
    updated = models.DateTimeField(null=True)
    posted_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    search_fields = [
        index.SearchField('degree_offered', partial_match=True),
        index.SearchField('school_name', partial_match=True),
        index.SearchField('education_description_new', partial_match=True),
        index.RelatedFields('region', [
            index.SearchField('name')
        ]),
        index.RelatedFields('city', [
            index.SearchField('name')
        ])
    ]

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        self.education_description_new = clean_html(
            self.education_description_new)

        return super(EducationPage, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('detail_education_post', args=[self.uuid])

    def __str__(self):
        return f"{self.school_name}, {self.degree_offered}"

    @property
    def expire_date(self):
        return self.updated + relativedelta(months=+6)
