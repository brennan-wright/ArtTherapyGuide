from blog.apps import BlogConfig
from blog.models import BlogAudience
from django.apps import apps
from django.test import TestCase

from tests.fixtures import BlogAudienceFactory


class BlogConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(BlogConfig.name, 'blog')
        self.assertEqual(apps.get_app_config(
            'blog').name, 'blog')


class BlogTestCaseViews(TestCase):
    @classmethod
    def setUp(cls):
        cls.blogaudience1 = BlogAudienceFactory()

    def test_directive_str(self):
        blogpage = self.blogaudience1
        abs = BlogAudience.__str__(blogpage)
        rev = blogpage.name
        self.assertEqual(abs, rev)
