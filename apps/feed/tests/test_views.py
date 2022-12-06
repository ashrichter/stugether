import pytz
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.datetime_safe import datetime

from apps.feed.models import Post


class TestCallsFeed(TestCase):
    """
    Tests for login/register/logout
    """
    def setUp(self):
        """
        Setting up test post and a test user.
        """

        testUser = get_user_model()
        self.user = testUser.objects.create_user(username='feed', email='feed@test.com', password='test', type=1)
        self.client = Client()
        Post.objects.create(title='test_post', content='test',
                            date_posted=datetime(2013, 11, 20, 20, 8, 7, 127325, tzinfo=pytz.UTC),
                            author=self.user, up_votes=2, down_votes=1)

    def test_context(self):
        """
        Testing if the post is getting passed to the feed page. This is done by checking if the first post has
        the title 'test_post' as set.
        """
        # GET response using the test client.
        response = self.client.get(reverse('home'))
        self.assertIsNotNone(response.context.get('posts'))
        # checking title
        testingPost = response.context.get('posts')[0]
        self.assertEqual(testingPost.title, 'test_post')

