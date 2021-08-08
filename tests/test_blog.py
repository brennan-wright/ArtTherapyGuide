from blog.apps import BlogConfig
from django.apps import apps
from django.test import TestCase


class BlogConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(BlogConfig.name, 'blog')
        self.assertEqual(apps.get_app_config(
            'blog').name, 'blog')
