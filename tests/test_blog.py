from blog.apps import BlogConfig
from blog.models import AuthorIndexPage, BlogAudience
from django.apps import apps
from django.contrib import auth
from django.test import TestCase
from django.urls.base import reverse
from wagtail.core.models import Page, Site

from tests.fixtures import (AboutPageFactory, AuthorIndexPageFactory,
                            AuthorPageFactory, BlogAudienceFactory,
                            BlogIndexPageFactory, ContactPageFactory,
                            HomePageFactory, PrivacyPolicyPageFactory)


class BlogConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(BlogConfig.name, 'blog')
        self.assertEqual(apps.get_app_config(
            'blog').name, 'blog')


class BlogTestCaseViews(TestCase):
    @classmethod
    def setUp(cls):
        cls.site = Site.objects.create(
            is_default_site=True, root_page=Page.get_first_root_node())
        cls.homepage = HomePageFactory()
        cls.authorindexpage = AuthorIndexPageFactory(parent=cls.homepage)
        cls.authorpage1 = AuthorPageFactory(parent=cls.authorindexpage)
        cls.authorpage2 = AuthorPageFactory(parent=cls.authorindexpage)
        cls.blogaudience = BlogAudienceFactory()
        cls.privacypage = PrivacyPolicyPageFactory(parent=cls.homepage)
        cls.aboutpage = AboutPageFactory(parent=cls.homepage)
        cls.contactpage = ContactPageFactory(parent=cls.homepage)
        cls.blogindexpage = BlogIndexPageFactory(parent=cls.homepage)

    def test_author_page_index(self):
        authorlist = self.authorindexpage
        response = self.client.get(
            authorlist.url)

        self.assertEqual(response.status_code, 200)

    def test_blog_audience_str(self):
        blogaudience = self.blogaudience
        abs = BlogAudience.__str__(blogaudience)
        rev = blogaudience.name
        self.assertEqual(abs, rev)


class BlogTestCaseViewNoFixtures(TestCase):
    @classmethod
    def setUp(cls):
        cls.site = Site.objects.create(
            is_default_site=True, root_page=Page.get_first_root_node())
        cls.homepage = HomePageFactory()
        cls.authorindexpage = AuthorIndexPageFactory(parent=cls.homepage)

    def test_author_page_index_no_fixtures(self):
        authorlist = self.authorindexpage
        response = self.client.get(
            authorlist.url,  {'page': 999, })

        self.assertEqual(response.context['posts'].number, 1)
