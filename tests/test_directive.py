
from directive.apps import DirectiveConfig
from directive.models import DirectivePage
from django.apps import apps
from django.test import TestCase
from django.urls import reverse

from tests.factories import (DirectiveThemeFactory, DirectivePageFactory,
                             DirectivePopulationFactory, UserFactory)


class DirectiveConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(DirectiveConfig.name, 'directive')
        self.assertEqual(apps.get_app_config(
            'directive').name, 'directive')


class DirectiveTestCaseViews(TestCase):
    @classmethod
    def setUp(cls):
        cls.population1 = DirectivePopulationFactory()
        cls.population2 = DirectivePopulationFactory()
        cls.theme1 = DirectiveThemeFactory()
        cls.theme2 = DirectiveThemeFactory()
        cls.posted_by = UserFactory()

        cls.directivepage = DirectivePageFactory(
            posted_by=cls.posted_by,
            population=(cls.population1, cls.population2),
            theme=(cls.theme1, cls.theme2),
        )

    def test_directive_index_view_url_exists_at_desired_location(self):
        response = self.client.get('/directives/')
        self.assertEqual(response.status_code, 200)

    def test_directive_index_view_url_accessible_by_name(self):
        response = self.client.get(reverse('list_directive_post'))
        self.assertEqual(response.status_code, 200)

    def test_directive_index_view_uses_correct_template(self):
        response = self.client.get(reverse('list_directive_post'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'directive/directive_index_page.html')

    def test_directive_edit_page_exists(self):
        user = self.posted_by
        directivepage = self.directivepage
        self.client.force_login(user=user)
        response = self.client.get(
            reverse('edit_directive_post', kwargs={'uuid': directivepage.uuid}))
        self.assertEqual(response.status_code, 200)

    def test_directive_absolute_url(self):
        directivepage = self.directivepage
        abs = DirectivePage.get_absolute_url(directivepage)
        rev = reverse('detail_directive_post', args=[directivepage.uuid])
        self.assertEqual(abs, rev)

    def test_directive_str(self):
        directivepage = self.directivepage
        abs = DirectivePage.__str__(directivepage)
        rev = directivepage.title
        self.assertEqual(abs, rev)

    def test_detail_directive_view(self):
        post = DirectivePage.objects.first()
        response = self.client.get(
            reverse('detail_directive_post', args=(post.uuid,)))
        self.assertEqual(response.status_code, 200)

    def test_thanks_directive_view(self):
        post = DirectivePage.objects.first()
        response = self.client.get(
            reverse('thanks_directive_post', args=(post.uuid,)))
        self.assertEqual(response.status_code, 200)

    def test_directive_create_page_exists(self):
        user = self.posted_by
        self.client.force_login(user=user)
        response = self.client.get(
            reverse('new_directive_post'))
        self.assertEqual(response.status_code, 200)

    def test_directive_delete_page_exists(self):
        user = self.posted_by
        directivepage = self.directivepage
        self.client.force_login(user=user)
        response = self.client.get(
            reverse('delete_directive_entry', args=[directivepage.uuid]))
        self.assertEqual(response.status_code, 200)


class DirectiveTestCaseViewMultiplePosts(TestCase):
    @classmethod
    def setUp(cls):
        cls.population1 = DirectivePopulationFactory()
        cls.population2 = DirectivePopulationFactory()
        cls.theme1 = DirectiveThemeFactory()
        cls.theme2 = DirectiveThemeFactory()
        cls.posted_by = UserFactory()

        cls.directivepage = DirectivePageFactory.create_batch(20,
                                                              posted_by=cls.posted_by,
                                                              population=(
                                                                  cls.population1, cls.population2),
                                                              theme=(
                                                                  cls.theme1, cls.theme2))

    def test_list_directive_view_search(self):
        searchq = DirectivePage.objects.first()
        response = self.client.get(reverse('list_directive_post'), {
            'search': searchq.title})
        self.assertEqual(response.status_code, 200)

    def test_list_directive_view_population(self):
        audienceq = DirectivePage.objects.first()
        response = self.client.get(reverse('list_directive_post'), {
            'population': audienceq.population})
        self.assertEqual(response.status_code, 200)

    def test_list_directive_view_theme(self):
        audienceq = DirectivePage.objects.first()
        response = self.client.get(reverse('list_directive_post'), {
            'theme': audienceq.theme})
        self.assertEqual(response.status_code, 200)
