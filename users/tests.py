from django.apps import apps
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from .apps import UsersConfig
from .forms import UserDeactivateForm, UserDeleteForm
from .views import ProfileView, UserDeleteView

# Create your tests here.


class UserConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(UsersConfig.name, 'users')
        self.assertEqual(apps.get_app_config(
            'users').name, 'users')


class UserTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='123abc', password='somepassword')

    def test_user_delete_view_get(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse("delete-profile"))
        url = reverse('delete-profile')
        self.assertEqual(response.status_code, 200)
        self.assertEquals(resolve(url).func.view_class,
                          UserDeleteView)
        self.assertTemplateUsed(response, 'users/user_deletion.html')

    def test_user_profile_view(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse("profile"))
        url = reverse('profile')
        self.assertEqual(response.status_code, 200)
        self.assertEquals(resolve(url).func,
                          ProfileView)

    def test_user_delete_profile_form(self):
        self.client.force_login(user=self.user)
        form = UserDeleteForm(data={'delete': True
                                    })
        response = self.client.post(
            reverse('delete-profile'), data={"delete": True}
        )
        redirecturl = "/"
        self.assertRedirects(response, redirecturl)
        self.assertTrue(form.is_valid())

    def test_user_delete_profile(self):
        self.client.force_login(user=self.user)
        response = self.client.post(
            reverse("delete-profile"), data={"delete": True})
        redirecturl = '/'
        self.assertRedirects(response, redirecturl)
        self.assertEqual(User.objects.count(), 0)

    def test_user_deactivate_form_invalid(self):
        self.client.force_login(user=self.user)
        form = UserDeactivateForm(data={'deactivate': ""
                                        })
        self.assertFalse(form.is_valid())

    def test_user_delete_form_invalid(self):
        self.client.force_login(user=self.user)
        form = UserDeleteForm(data={'delete': ""
                                    })
        self.assertFalse(form.is_valid())
