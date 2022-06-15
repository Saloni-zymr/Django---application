from rest_framework.test import APITestCase
from flights.models import User


class TestModel(APITestCase):

    def test_raise_error_when_email_is_not_given(self):
        self.assertRaises(ValueError, User.objects.create_user,
                          email="",
                          name="me",
                          contact_number=68,
                          gender=1,
                          address="abc",
                          state="Guj",
                          city="surat",
                          country="India",
                          pincode=68,
                          dob="2001-01-01",
                          password="me"
                          )

    def test_raise_error_message_when_email_is_not_given(self):
        with self.assertRaisesMessage(ValueError, 'User must have an email address'):
            User.objects.create_user(
                email="",
                name="me",
                contact_number=68,
                gender=1,
                address="abc",
                state="Guj",
                city="surat",
                country="India",
                pincode=68,
                dob="2001-01-01",
                password="me"
            )

    def test_create_user(self):
        user = User.objects.create_user("me@a.com", "me", 68, 1, "abc", "Guj", "surat", "India", 68, "2001-01-01", "me")
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, 'me@a.com')

    def test_create_superuser(self):
        user = User.objects.create_superuser("as@a.com", "as", 32, 1, "asd", "as", "as", "as", 23, "2019-10-12", "as")
        self.assertIsInstance(user, User)
        self.assertTrue(user.is_admin)
        self.assertEqual(user.email, 'as@a.com')

    def test_has_perm(self):
        user = User.objects.create_user("as@a.com", "as", 32, 1, "asd", "as", "as", "as", 23, "2019-10-12", "as")
        self.assertIsInstance(user, User)
        self.assertEqual(user.is_staff, user.is_admin)
        self.assertFalse(user.is_admin)

    def test_create_user_model(self):
        user = User.objects.create_user("me@a.com", "me", 68, 1, "abc", "Guj", "surat", "India", 68, "2001-01-01", "me")
        self.assertEqual(user.__str__(), 'me@a.com')

    def test_has_perm_user(self):
        user = User.objects.create_user("me@a.com", "me", 68, 1, "abc", "Guj", "surat", "India", 68, "2001-01-01", "me")
        self.assertEqual(user.has_perm(user.is_admin), False)

    def test_has_module_perm_user(self):
        user = User.objects.create_user("me@a.com", "me", 68, 1, "abc", "Guj", "surat", "India", 68, "2001-01-01", "me")
        self.assertEqual(user.has_module_perms(user.is_admin), True)

    # def test_flight_details_model(self):
    #     flight = FlightDetails.objects.get(1, "abc", "air", "05:56:59", "2022-06-08", "05:57:50", "B", 6800, "surat", "Bang", 1, 890, 100)
    #     # self.assertIsInstance(flight, FlightDetails)
    #     self.assertEqual(flight.__str__(), "abc")
