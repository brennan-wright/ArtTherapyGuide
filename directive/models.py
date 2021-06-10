import uuid

import bleach
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from tinymce import models as tinymce_models
from versatileimagefield.fields import VersatileImageField
from wagtail.search import index


def clean_html(html):
    authorized_tags = [
        'p', 'h3', 'strong', 'em',
        'i', 'b'
    ]
    authorized_attributes = {}

    return bleach.clean(
        html, authorized_tags, authorized_attributes, strip=True)


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


class DirectiveAudience(models.Model):
    name = models.CharField(max_length=250, verbose_name="Audience Name")

    def __str__(self):
        return self.name


class DirectivePage(index.Indexed, models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        verbose_name="Random string for url",
    )
    title = models.CharField(
        max_length=250,
        verbose_name="Name or title of directive.")
    population = models.ManyToManyField(
        DirectivePopulation, related_name='educationposts',
        verbose_name="Who is the target population?")
    diagnosis = models.ManyToManyField(
        DirectiveDiagnosis, related_name='educationposts',
        verbose_name="What is the target diagnosis?")
    audience = models.ManyToManyField(
        DirectiveAudience, related_name='educationposts',
        verbose_name="Who is the target audience for this post?")
    directive_description = tinymce_models.HTMLField(null=True)
    created = models.DateTimeField(null=True, editable=False)
    updated = models.DateTimeField(null=True)
    posted_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    search_fields = [
        index.SearchField('title', partial_match=True),
        index.SearchField('directive_description', partial_match=True),
        index.SearchField('posted_by', partial_match=True),
        index.RelatedFields('population', [
            index.SearchField('name')
        ]),
        index.RelatedFields('audience', [
            index.SearchField('name')
        ]),
        index.RelatedFields('diagnosis', [
            index.SearchField('name')
        ])
    ]

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        self.directive_description = clean_html(
            self.directive_description)
        return super(DirectivePage, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('detail_directive_post', args=[self.uuid])

    def __str__(self):
        return f"{self.title}"


class DirectiveImages(models.Model):
    post = models.ForeignKey(
        DirectivePage, default=None, on_delete=models.CASCADE)
    image = VersatileImageField(
        'Image',
        upload_to='directive_images/original/',
        width_field='width',
        height_field='height')
    height = models.PositiveIntegerField(
        'Image Height',
        blank=True,
        null=True
    )
    width = models.PositiveIntegerField(
        'Image Width',
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        try:
            this = DirectiveImages.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete_all_created_images()
                this.image.delete(save=False)
        except:
            pass
        super(DirectiveImages, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Directive Image'
        verbose_name_plural = 'Directive Images'


@receiver(models.signals.post_delete, sender=DirectiveImages)
def delete_DirectiveImagesModel_images(sender, instance, **kwargs):
    """
    Deletes ExampleImageModel image renditions on post_delete.
    """
    # Deletes Image Renditions
    instance.image.delete_all_created_images()
    # Deletes Original Image
    instance.image.delete(save=False)
