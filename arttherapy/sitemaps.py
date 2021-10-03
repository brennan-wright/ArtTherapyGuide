from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class AboutSitemap(Sitemap):

    def items(self):
        return ['about']

    def location(self, item):
        return reverse(item)


class HomeSitemap(Sitemap):

    def items(self):
        return ['home']

    def location(self, item):
        return reverse(item)


class DirectiveIndexSitemap(Sitemap):

    def items(self):
        return ['list_directive_post']

    def location(self, item):
        return reverse(item)


class DirectiveNewSitemap(Sitemap):

    def items(self):
        return ['new_directive_post']

    def location(self, item):
        return reverse(item)


class LoginSitemap(Sitemap):

    def items(self):
        return ['account_login']

    def location(self, item):
        return reverse(item)


class SignupSitemap(Sitemap):

    def items(self):
        return ['account_signup']

    def location(self, item):
        return reverse(item)


class ProfileSitemap(Sitemap):

    def items(self):
        return ['profile']

    def location(self, item):
        return reverse(item)
