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


class DirectivePage(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        verbose_name="Random string for url",)
    title = models.CharField(
        max_length=75,
        verbose_name="Name or title of directive")
    population = models.ManyToManyField(
        DirectivePopulation, related_name='educationposts',
        verbose_name="Who is the target population?")
    diagnosis = models.ManyToManyField(
        DirectiveDiagnosis, related_name='educationposts',
        verbose_name="What is the target DSM5 diagnosis?")
    intro = models.TextField(max_length=300, blank=False, null=True,
                             verbose_name="A short intorduction that describes your directive")
    discussion = models.TextField(max_length=300, blank=False, null=True,
                                  verbose_name="How would you lead the duscussion with the client?")
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
        return self.title


class DirectiveObjective(models.Model):
    objective = models.CharField(
        max_length=250, verbose_name="List of objectives for a particular directive", null=False, blank=False)
    directive = models.ForeignKey(
        DirectivePage, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.objective
