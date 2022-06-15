from django.test import SimpleTestCase
from django.urls import reverse, resolve
from knox.views import LoginView, LogoutView, LogoutAllView
from flights.views import RegisterAPI, UserAPI, ChangePasswordView


class TestUrls(SimpleTestCase):

    def test_register_url(self):
        url = reverse('register')
        # print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, RegisterAPI)

    def test_login_url(self):
        url = reverse('login')
        # print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, LoginView)

    def test_logout_url(self):
        url = reverse('logout')
        # print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, LogoutView)

    def test_logout_all_url(self):
        url = reverse('logoutall')
        # print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, LogoutAllView)

    def test_user_url(self):
        url = reverse('user')
        # print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, UserAPI)

    def test_change_password_url(self):
        url = reverse('change-password')
        # print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, ChangePasswordView)
