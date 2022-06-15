from rest_framework.test import APITestCase
from django.urls import reverse
from faker import Faker


class TestSetUp(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.fake = Faker()

        self.user_data = {
            "name": self.fake.name(),
            "email": self.fake.email(),
            "password": self.fake.password(),
            "contact_number": 78,
            "gender": 1,
            "address": "bavh",
            "state": "Guj",
            "city": "surat",
            "country": "India",
            "pincode": 68,
            "dob": "2001-01-01"
        }

        self.log_data = {
            "email": "cv@a.com",
            "password": "cv"
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
