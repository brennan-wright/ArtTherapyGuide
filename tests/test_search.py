
from django.apps import apps
from django.test import TestCase
from django.urls import reverse
from search.apps import SearchConfig


class SearchConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(SearchConfig.name, 'search')
        self.assertEqual(apps.get_app_config(
            'search').name, 'search')


class SearchTestCase(TestCase):
    def test_search_view_url_exists_at_desired_location(self):
        response = self.client.get('/search/')
        self.assertEqual(response.status_code, 200)

    def test_search_view_url_accessible_by_name(self):
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)

    def test_search_view_uses_correct_template(self):
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/search.html')

    def test_search_view_get_url_exists_at_desired_location(self):
        response = self.client.get('/search/?query=funhaus')
        self.assertEqual(response.status_code, 200)
