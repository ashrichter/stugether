from django.db import models

from apps.core.models import User
from apps.feed.models import Post


class Notification(models.Model):
    FRIEND = 'friend'
    REACT = 'react'
    COMMENT = 'comment'
    MESSAGE = 'message'
    MENTION = 'mention'

    CHOICES = (
        (FRIEND, 'Friend request'),
        (REACT, 'React'),
        (COMMENT, 'Comment'),
        (MESSAGE, 'Message'),
        (MENTION, 'Mention')
    )

    to_user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)

    notification_type = models.CharField(max_length=20, choices=CHOICES)
    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='creatednotifications', on_delete=models.CASCADE)

    # the post linking to the notification
    post = models.ForeignKey(Post, related_name='notification', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']
