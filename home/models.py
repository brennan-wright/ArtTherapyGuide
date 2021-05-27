from blog.models import BlogPage
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (FieldPanel, FieldRowPanel,
                                         InlinePanel, MultiFieldPanel,
                                         PageChooserPanel)
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtailcaptcha.models import WagtailCaptchaEmailForm


class HomePage(Page):
    '''
    Homepage model. Contains the featured post and main structure for the hierarchy of pages.
    '''
    subpage_types = [
        'blog.BlogIndexPage',  # appname.ModelName
        'home.AboutPage',  # appname.ModelName
        'home.PrivacyPolicyPage',  # appname.ModelName
        'blog.AuthorIndexPage',  # appname.ModelName
        'home.ContactPage',  # appname.ModelName



    ]
    parent_page_type = ['wagtailcore.Page']
    template = "home/home_page.html"
    max_count = 1
    featured_post = models.ForeignKey(
        "blog.BlogPage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        PageChooserPanel("featured_post"),

    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        first_six_posts = BlogPage.objects.live(
        ).public().order_by('-first_published_at')[:6]

        context["first_six_posts"] = first_six_posts
        return context


class AboutPage(Page):
    '''
    About page model
    '''
    subpage_types = []
    template = "home/about_page.html"
    max_count = 1
    icon = "edit"
    label = "About Page"
    body = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('body'),

    ]


class PrivacyPolicyPage(Page):
    '''
    Privacy page model
    '''
    subpage_types = []
    template = "home/privacy_policy_page.html"
    max_count = 1
    icon = "edit"
    label = "Privacy Page"
    body = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]


class ContactFormField(AbstractFormField):
    page = ParentalKey(
        'ContactPage',
        on_delete=models.CASCADE,
        related_name='form_fields',
    )


class ContactPage(WagtailCaptchaEmailForm):
    subpage_types = []
    max_count = 1
    template = "home/contact_page.html"

    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro'),
        InlinePanel('form_fields', label='Form Fields'),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6")
            ]),
            FieldPanel("subject"),
        ], heading="Email Settings"
        ),

    ]
