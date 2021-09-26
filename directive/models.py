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
        verbose_name="Directive Title")
    population = models.ManyToManyField(
        DirectivePopulation, related_name='educationposts',
        verbose_name="Target Population", help_text="*Use ctrl+click on windows, or cmd+click on a Mac to select more than one.")
    diagnosis = models.ManyToManyField(
        DirectiveDiagnosis, related_name='educationposts',
        verbose_name="Target Diagnosis", help_text="*Use ctrl+click on windows, or cmd+click on a Mac to select more than one.")
    intro = models.TextField(max_length=300, blank=False, null=True,
                             verbose_name="Directive Introduction")
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
        max_length=250, verbose_name="Directive Objectives", null=False, blank=False)
    directive = models.ForeignKey(
        DirectivePage, on_delete=models.CASCADE, related_name='objectives', null=False, blank=False)

    def __str__(self):
        return self.objective


class DirectiveMaterial(models.Model):
    material = models.CharField(
        max_length=250, verbose_name="Directive Materials", null=False, blank=False)
    directive = models.ForeignKey(
        DirectivePage, on_delete=models.CASCADE, related_name='materials', null=False, blank=False)

    def __str__(self):
        return self.material


class DirectiveInstruction(models.Model):
    instruction = models.CharField(
        max_length=250, verbose_name="Directive Instruction", null=False, blank=False)
    directive = models.ForeignKey(
        DirectivePage, on_delete=models.CASCADE, related_name='instructions', null=False, blank=False)

    def __str__(self):
        return self.instruction
