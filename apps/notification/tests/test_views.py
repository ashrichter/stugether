from django.urls import reverse


def test_call_notifications(self):
    """
    Tests if edit profile page is accessible when logged in and should redirect to home page when not logged in.
    """
    self.client.login(username='test', password='test')
    response = self.client.post(reverse('notifications', args=[self.user.username]))
    self.assertTemplateUsed(response, 'notification/notifications.html')
    # test when logged out
    self.client.logout()
    response_invalid = self.client.post(reverse('notifications', args=[self.user.username]))
    self.assertRedirects(response_invalid, '/')