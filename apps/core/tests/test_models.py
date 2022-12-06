from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.core.models import Friend, User


class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(username='user', email='normal@user.com', password='foo', type=1)
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.username, 'user')
        self.assertEqual(user.type, 1)
        try:
            self.assertIsNone(user.institution)
            self.assertIsNone(user.field_of_study)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser('admin', 'super@user.com', 'foo', type=1)
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertEqual(admin_user.username, 'admin')
        self.assertEqual(admin_user.type, 1)
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class FriendManagementTest(TestCase):
    def setUp(self):
        User.objects.create(username='user1', email='normal1@user.com',
                            password='foo', type=1)
        User.objects.create(username='user2', email='normal2@user.com',
                            password='foo', type=1)

    def test_create_friend(self):
        user1 = User.objects.get(username='user1')
        user2 = User.objects.get(username='user2')
        friend = Friend.objects.create(sender=user1, receiver=user2)
        self.assertFalse(friend.accepted)
        self.assertFalse(friend.is_accepted())
        self.assertEqual(friend.sender, user1)
        self.assertEqual(friend.receiver, user2)
        friend.accepted = True
        friend.save()
        self.assertTrue(friend.accepted)
