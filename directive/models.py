import uuid

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class DirectiveDiagnosis(models.Model):
    name = models.CharField(
        max_length=250, verbose_name="Applicable diagnosis for directive")

    def __str__(self):
        return self.name


class DirectivePopulation(models.Model):
    name = models.CharField(
        max_length=250, verbose_name="Applicable population for directive")

    def __str__(self):
        return self.name


class DirectiveIdentifiedPatient(models.Model):
    name = models.CharField(max_length=250, verbose_name="Identified Patient")

    def __str__(self):
        return self.name


class DirectiveAudience(models.Model):
    name = models.CharField(max_length=250, verbose_name="Audience Name")

    def __str__(self):
        return self.name


class DirectivePage(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        verbose_name="Random string for url",)
    title = models.CharField(
        max_length=250,
        verbose_name="Name or title of directive.")
    population = models.ManyToManyField(
        DirectivePopulation, related_name='educationposts',
        verbose_name="Who is the target population?")
    diagnosis = models.ManyToManyField(
        DirectiveDiagnosis, related_name='educationposts',
        verbose_name="What is the target DSM5 diagnosis?")
    identified_patient = models.ManyToManyField(
        DirectiveIdentifiedPatient, related_name='educationposts',
        verbose_name="Who is the target identified patient?")
    audience = models.ManyToManyField(
        DirectiveAudience, related_name='educationposts',
        verbose_name="Who is the target audience for this post?")
    created = models.DateTimeField(null=True, editable=False)
    updated = models.DateTimeField(null=True)
    posted_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super(DirectivePage, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('detail_directive_post', args=[self.uuid])

    def __str__(self):
        return f"{self.title}"
