from .test_setup import TestSetUp


class TestView(TestSetUp):
    def test_user_cannot_register_with_no_data(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, 400)

    def test_user_can_register_correctly(self):
        res = self.client.post(
            self.register_url, self.user_data, format="json")
        self.assertEqual(res.status_code, 200)

    def test_user_cannot_login(self):
        self.client.post(
            self.login_url, self.user_data, format="json")
        res = self.client.post(self.login_url, self.log_data, format="json")
        self.assertEqual(res.status_code, 401)

    # def test_user_can_login(self):
    #     pass


