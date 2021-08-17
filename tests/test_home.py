from blog.models import AuthorIndexPage, AuthorPage, BlogIndexPage, BlogPage
from home.models import AboutPage, ContactPage, HomePage, PrivacyPolicyPage
from wagtail.tests.utils import WagtailPageTests


class HomePageTests(WagtailPageTests):
    def test_can_create_under_home_page(self):
        # You can create a ContentPage under a HomePage
        self.assertCanCreateAt(HomePage, AboutPage)
        self.assertCanCreateAt(HomePage, PrivacyPolicyPage)
        self.assertCanCreateAt(HomePage, ContactPage)
        self.assertCanCreateAt(HomePage, BlogIndexPage)
        self.assertCanCreateAt(HomePage, AuthorIndexPage)

#    def test_can_not_create_under_home_page(self):
#        # You can create a ContentPage under a HomePage
#        self.assertCanNotCreateAt(HomePage, BlogPage)
#        self.assertCanNotCreateAt(HomePage, AuthorPage)
#        self.assertCanNotCreateAt(HomePage, ContactPage)
