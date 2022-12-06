import pytz
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.datetime_safe import datetime
from apps.core.models import User
from apps.feed.models import Post, User, Comment


class PostManagersTests(TestCase):

    def test_create_post(self):
        test_user = User.objects.create_user(username='user', email='normal@user.com', password='foo', type=1)
        post = Post.objects.create(title='test_post2', content='test',
                                   date_posted=datetime(2013, 12, 13, 14, 4, 9, 127325, tzinfo=pytz.UTC),
                                   author=test_user, up_votes=9, down_votes=100)
        self.assertEqual(post.title, 'test_post2')
        self.assertEqual(post.content, 'test')
        self.assertEqual(post.date_posted, datetime(2013, 12, 13, 14, 4, 9, 127325, tzinfo=pytz.UTC))
        self.assertEqual(post.author, test_user)
        self.assertEqual(post.up_votes, 9)
        self.assertEqual(post.down_votes, 100)

    def test_comment_post(self):
        test_user = User.objects.create_user(username='user', email='normal@user.com', password='foo', type=1)
        post = Post.objects.create(title='test_post2', content='test',
                                   date_posted=datetime(2013, 12, 13, 14, 4, 9, 127325, tzinfo=pytz.UTC),
                                   author=test_user, up_votes=9, down_votes=100)
        comment = Comment.objects.create(user=test_user,
                                                 created_at=datetime(2013, 12, 13, 14, 4, 9, 127325, tzinfo=pytz.UTC),
                                                 post=post, body='This is a comment')
        self.assertEqual(comment.body, 'This is a comment')
