from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.shortcuts import render
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import ItemBase, TagBase
from wagtail.admin.edit_handlers import (FieldPanel, MultiFieldPanel,
                                         PageChooserPanel, StreamFieldPanel)
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet


@register_snippet
class BlogAudience(models.Model):
    name = models.CharField(max_length=250, verbose_name="Audience Name")

    def __str__(self):
        return self.name


@register_snippet
class BlogTag(TagBase):
    free_tagging = False

    class Meta:
        verbose_name = "blog tag"
        verbose_name_plural = "blog tags"


class TaggedBlog(ItemBase):
    tag = models.ForeignKey(
        BlogTag, related_name="tagged_blogs", on_delete=models.CASCADE
    )
    content_object = ParentalKey(
        to='blog.BlogPage',
        on_delete=models.CASCADE,
        related_name='tagged_items'
    )


class BlogIndexPage(Page):
    """Page to list all blog posts"""
    max_count = 1
    subpage_types = [
        'blog.BlogPage',  # ModelName

    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super(BlogIndexPage, self).get_context(request)
        # blogpages = self.get_children().live().order_by("-first_published_at")
        blogpages = BlogPage.objects.child_of(self).live()

        tag = request.GET.get('tag')
        if tag:
            blogpages = blogpages.filter(tags__name=tag).all()
            context['tag'] = BlogTag.objects.get(name=tag).name

        paginator = Paginator(blogpages, 10)

        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context['posts'] = posts
        return context

    def get_sitemap_urls(self, request):
        sitemap = super().get_sitemap_urls(request)

        return sitemap


class BlogPage(Page):
    subpage_types = []
    date = models.DateField(
        verbose_name="Post date",
        help_text='The date that the end user sees as the date that the article was posted.',
    )
    intro = models.CharField(
        max_length=250,
        verbose_name="Introduction",
        help_text='A short 250 character description of the article. This is generally just the first paragraph of the article.',
    )
    body = StreamField([
        ('subheading', blocks.CharBlock()),
        ('paragraph', blocks.RichTextBlock(
            features=['bold', 'italic', 'link'])),
        ('image', ImageChooserBlock())])
    audience = models.ManyToManyField(
        BlogAudience, related_name='blogposts',
        verbose_name="Who is the target audience?")
    tags = ClusterTaggableManager(through=TaggedBlog, blank=True)
    author = models.ForeignKey(
        "blog.AuthorPage", on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.SET_NULL, related_name="+", null=True)

    def get_absolute_url(self):
        return self.get_url()

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("date"),
                PageChooserPanel("author"),
            ],
            heading="Blog information",
        ),
        FieldPanel("intro"),
        FieldPanel('tags'),
        StreamFieldPanel("body"),

        ImageChooserPanel("image"),
    ]


class AuthorPage(Page):
    subpage_types = []
    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    body = StreamField([
        ('subheading', blocks.CharBlock()),
        ('paragraph', blocks.RichTextBlock(
            features=['bold', 'italic', 'link'])),
        ('image', ImageChooserBlock())], null=True)
    linkedin = models.URLField(max_length=200, null=True, blank=True)
    twitter = models.URLField(max_length=200, null=True, blank=True)
    website = models.URLField(max_length=200, null=True, blank=True)
    photo = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.SET_NULL, null=True, related_name="+")

    content_panels = Page.content_panels + [
        FieldPanel("first_name"),
        FieldPanel("last_name"),
        StreamFieldPanel("body"),
        FieldPanel("linkedin"),
        FieldPanel("twitter"),
        FieldPanel("website"),
        ImageChooserPanel("photo"),

    ]


class AuthorIndexPage(Page):
    subpage_types = [
        'blog.AuthorPage',  # app.ModelName
    ]
    max_count = 1

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super(AuthorIndexPage, self).get_context(request)
        # blogpages = self.get_children().live().order_by("-first_published_at")
        blogpages = AuthorPage.objects.child_of(self).live()

        paginator = Paginator(blogpages, 10)

        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context['posts'] = posts
        return context
