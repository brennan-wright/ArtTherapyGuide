import uuid

from cities_light.models import City, Region
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from wagtail.search import index


class EducationLevel(models.Model):
    name = models.CharField(
        max_length=250, verbose_name="Education Level Name")

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
    education_level = models.ManyToManyField(
        EducationLevel, related_name='educationposts',
        verbose_name="What is the level of education that will be acheived after attending?")
    school_url = models.URLField(
        max_length=250,
        blank=True,
        verbose_name="URL to School or Company")
    region = models.ForeignKey(
        Region, null=True, on_delete=models.SET_NULL, verbose_name="Region",)
    city = models.ForeignKey(
        City, null=True, on_delete=models.SET_NULL, verbose_name="City",)
    remote = models.BooleanField(
        verbose_name="Does this School or Company offer remote learning?")
    created = models.DateTimeField(null=True, editable=False)
    updated = models.DateTimeField(null=True)
    posted_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    search_fields = [
        index.SearchField('school_name', partial_match=True),
        index.RelatedFields('region', [
            index.SearchField('name')
        ]),
        index.RelatedFields('city', [
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

        return super(EducationPage, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('detail_education_post', args=[self.uuid])

    def __str__(self):
        return f"{self.school_name}"

    @ property
    def expire_date(self):
        return self.updated + relativedelta(months=+6)
