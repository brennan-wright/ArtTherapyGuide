from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class AboutSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5
    protocol = "https"

    def items(self):
        return ['about']

    def location(self, item):
        return reverse(item)


class HomeSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5
    protocol = "https"

    def items(self):
        return ['home']

    def location(self, item):
        return reverse(item)


class DirectiveIndexSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5
    protocol = "https"

    def items(self):
        return ['list_directive_post']

    def location(self, item):
        return reverse(item)


class DirectiveNewSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5
    protocol = "https"

    def items(self):
        return ['new_directive_post']

    def location(self, item):
        return reverse(item)


class LoginSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5
    protocol = "https"

    def items(self):
        return ['account_login']

    def location(self, item):
        return reverse(item)


class SignupSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5
    protocol = "https"

    def items(self):
        return ['account_signup']

    def location(self, item):
        return reverse(item)


class ProfileSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5
    protocol = "https"

    def items(self):
        return ['profile']

    def location(self, item):
        return reverse(item)
