

from cities_light.models import City, Country, Region, SubRegion
from django.apps import apps
from django.test import TestCase
from django.urls import reverse
from education.apps import EducationConfig

from .fixtures import EducationLevelFactory, EducationPageFactory, UserFactory


class EducationConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(EducationConfig.name, 'education')
        self.assertEqual(apps.get_app_config(
            'education').name, 'education')


class EducationTestCase(TestCase):
    @classmethod
    def setUp(cls):
        cls.education_level1 = EducationLevelFactory()
        cls.education_level2 = EducationLevelFactory()
        cls.posted_by = UserFactory()
        cls.educationpage = EducationPageFactory(
            posted_by=cls.posted_by,
            education_level=(cls.education_level1, cls.education_level2))

    def test_education_index_view_url_exists_at_desired_location(self):
        response = self.client.get('/education/')
        self.assertEqual(response.status_code, 200)

    def test_education_index_view_url_accessible_by_name(self):
        response = self.client.get(reverse('list_education_post'))
        self.assertEqual(response.status_code, 200)

    def test_education_index_view_uses_correct_template(self):
        response = self.client.get(reverse('list_education_post'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'education/education_index_page.html')

    def test_education_single_post_exists(self):
        educationpage = self.educationpage
        response = self.client.get(
            reverse('detail_education_post', kwargs={'uuid': educationpage.uuid}))
        self.assertEqual(response.status_code, 200)

    def test_education_thanks_page_exists(self):
        educationpage = self.educationpage
        response = self.client.get(
            reverse('thanks_education_post', kwargs={'uuid': educationpage.uuid}))
        self.assertEqual(response.status_code, 200)

    def test_education_delete_page_exists(self):
        user = self.posted_by
        educationpage = self.educationpage
        self.client.force_login(user=user)
        response = self.client.get(
            reverse('delete_education_entry', kwargs={'uuid': educationpage.uuid}))
        self.assertEqual(response.status_code, 200)

    def test_education_edit_page_exists(self):
        user = self.posted_by
        educationpage = self.educationpage
        self.client.force_login(user=user)
        response = self.client.get(
            reverse('edit_education_post', kwargs={'uuid': educationpage.uuid}))
        self.assertEqual(response.status_code, 200)
