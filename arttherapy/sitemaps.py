from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    protocol = 'https'

    def items(self):
        return ['list_education_post', 'list_directive_post']

    def location(self, item):
        return reverse(item)
