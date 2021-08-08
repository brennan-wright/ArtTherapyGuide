from django.test import TestCase


class ArtTherapyTestCase(TestCase):
    def test_arttherapy_view_url_exists_at_desired_location(self):
        response = self.client.get('/health_check/')
        self.assertEqual(response.status_code, 200)
