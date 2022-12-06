from datetime import datetime

import pytz
from django.contrib.auth import get_user_model
from django.test import TestCase, Client, RequestFactory

from apps.feed.models import Post


class TestURLS(TestCase):
    """
    Testing URLS for feed
    """
    def setUp(self):
        """
        Setting up test post and a test user.
        """
        self.factory = RequestFactory()
        testUser = get_user_model()
        self.user = testUser.objects.create_user(username='feed', email='feed@test.com', password='test', type=1)
        self.client = Client()
        Post.objects.create(title='test_post', content='test',
                            date_posted=datetime(2013, 11, 20, 20, 8, 7, 127325, tzinfo=pytz.UTC),
                            author=self.user, up_votes=2, down_votes=1)

    def test_feed_page(self):
        """
        Test for feed page url.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_post_detail_page(self):
        """
        Test for post detail page url.
        """
        response = self.client.get('/post/1/')
        self.assertEqual(response.status_code, 200)

    def test_post_new_page(self):
        """
        Test for new post page url.
        """
        response = self.client.get('/post/new/')
        self.assertEqual(response.status_code, 200)
