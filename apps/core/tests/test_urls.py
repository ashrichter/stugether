from django.contrib.auth import get_user_model
from django.test import TestCase, Client, RequestFactory


class TestURLS(TestCase):
    """
    Testing URLS for core
    """
    def setUp(self):
        self.factory = RequestFactory()
        testUser = get_user_model()
        self.user = testUser.objects.create_user(username='core', email='core@test.com', password='test', type=1)
        self.client = Client()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_edit_profile_page(self):
        response = self.client.get('/edit-profile/')
        self.assertEqual(response.status_code, 302)

    def test_edit_profile_page(self):
        response = self.client.get('/core/profile/')
        self.assertEqual(response.status_code, 302)

    def test_following_topics_page(self):
        response = self.client.get('/core/following-topics/')
        self.assertEqual(response.status_code, 200)

    def test_friends_page(self):
        response = self.client.get('/core/friends/')
        self.assertEqual(response.status_code, 200)

    def test_select_topics_page(self):
        response = self.client.get('/select-topics/')
        self.assertEqual(response.status_code, 302)

    def test_register_page(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        # testing login
        response_login = self.client.post('/login/', {'username': 'core', 'password': 'test'})
        self.assertEqual(response_login.status_code, 302)

    def test_logout_page(self):
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)
