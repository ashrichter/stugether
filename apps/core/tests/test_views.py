from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, Client
from django.urls import reverse


class TestCallsCore(TestCase):
    """
    Tests for login/register/logout
    """
    def setUp(self):
        """
        Setting up a test user.
        """
        testUser = get_user_model()
        self.user = testUser.objects.create_user(username='test', email='test@user.com', password='test', type=1)
        self.client = Client()

    def test_call_login(self):
        """
        If post request has correct info then redirect to home page otherwise checks if renders login template.
        """
        # checking for get
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/login.html')
        # checking for post request
        response_post = self.client.post(reverse('login'), {'username': 'test', 'password': 'test'})
        self.assertEqual(response_post.status_code, 302)
        self.assertRedirects(response_post, '/')
        # checking for post request with invalid info
        response_post_invalid = self.client.post(reverse('login'), {'username': 'test', 'password': 'invalid'})
        self.assertEqual(response_post_invalid.status_code, 302)
        self.assertRedirects(response_post_invalid, '/')

    def test_call_register(self):
        """
        If post request then tests for redirect to login page or register page depending on whether info is correct
        and filled otherwise checks if renders register page.
        """
        # checking for get
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/register.html')
        # checking for post
        response_post = self.client.post(reverse('register'), {'username': 'test', 'password': 'test'})
        self.assertEqual(response_post.status_code, 200)
        self.assertTemplateUsed(response_post, 'core/register.html')


class TestCallsProfile(TestCase):
    """
    Tests for profile/user
    """
    def setUp(self):
        """
        Setting up a test user.
        """
        testUser = get_user_model()
        self.user = testUser.objects.create_user(username='test', email='test@user.com', password='test', type=1)
        self.client = Client()

    def test_call_profile_view_deny_anonymous(self):
        """
        Tests if anonymousUser profile redirects to home page.
        """
        response = self.client.get('/anonymousUser/profile/', follow=True)
        self.assertRedirects(response, '/')

    def test_call_profile_view_load(self):
        """
        Tests if profile page of the given user loads and invalid user page should return a not found error.
        """
        self.client.login(username='test', password='test')
        response = self.client.get('/test/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/profile.html')
        # tests for invalid user
        try:
            response_invalid = self.client.get('/invalid/profile/')
            self.assertEqual(response_invalid.status_code, 404)
        except ObjectDoesNotExist:
            pass

    def test_call_edit_profile(self):
        """
        Tests if edit profile page is accessible when logged in and should redirect to home page when not logged in.
        """
        self.client.login(username='test', password='test')
        response = self.client.post(reverse('edit-profile'))
        self.assertTemplateUsed(response, 'core/profile_edit.html')
        # when logged out
        self.client.logout()
        response_invalid = self.client.post(reverse('edit-profile'))
        self.assertRedirects(response_invalid, '/')

    def test_call_profile_following_topics(self):
        """
        Tests if profile following topic page is accessible when logged in and should still be able to view while
        logged out.
        """
        self.client.login(username='test', password='test')
        response = self.client.post(reverse('following-topics', args=[self.user.username]))
        self.assertTemplateUsed(response, 'core/profile_following_topics.html')
        # when logged out
        self.client.logout()
        response_invalid = self.client.post(reverse('following-topics', args=[self.user.username]))
        self.assertTemplateUsed(response_invalid, 'core/profile_following_topics.html')

    def test_call_profile_friends(self):
        """
        Tests if profile friends page for given user is accessible.
        """
        response = self.client.post(reverse('friends', args=[self.user.username]))
        self.assertTemplateUsed(response, 'core/profile_friends.html')

