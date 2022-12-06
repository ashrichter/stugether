from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from apps.core.models import User, Topic


class Post(models.Model):
    """ This class holds the details about the Post table in the database.

        A Post instance represents a post created by a user, its linked to both students and academics,
        you can like and dislike posts, you can put content, and attach files  .
        Fields:
        title: title of the post
        content: content of the post
        attachment: file attached to the post
        date_posted: date posted
        author: User(FK), author of the post
        up_votes: likes on the post
        down_votes: dislikes on the post
    """
    title = models.CharField(max_length=100)
    content = models.TextField()
    # TODO: Upload Directory should be users/attachments
    attachment = models.FileField(null=True, blank=True, upload_to='attachments', max_length=100)
    # profile_image = models.ImageField(null=True, blank=True, upload_to='images', default='default.jpg')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    up_votes = models.PositiveIntegerField(default=0)
    down_votes = models.PositiveIntegerField(default=0)

    # votes = models.IntegerField() The counter for upvote and down vote on this post.

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Vote(models.Model):
    """ This class holds the details about the Vote table in the database.

        A Vote instance links a user to the post he voted on, in order to track user
        preference
        Fields:
        user: User(FK): user that votes
        type: whether the user voted thumbs up or down
        post: Post(FK): post the user has voted on.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    UP = 1
    DOWN = 2
    TYPE = (
        (UP, _("Up")),
        (DOWN, _("Down")),
    )
    type = models.PositiveSmallIntegerField(choices=TYPE, default=UP)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Report(models.Model):
    """ This class holds the details about the Report table in the database.

        A Report instance allows admins to track and manage post based on user reports
        and can be linked to both users and academics.
        Fields:
        post: Post(FK): post that has been reported
        reporter: User(FK): user that reports the post
        date_reported: #Char(2): date the user reported the post
        description: Why it has been reported
        investigated: Whether or not a post has been investigated
        removed: Whether or not the post has been removed.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    date_reported = models.DateTimeField(default=timezone.now)
    MISLEADING = 1
    ILLEGAL = 2
    FRAUD = 3
    VIOLENT = 4
    HATE_SPEECH = 5
    HARASSMENT = 7
    OTHER = 8
    REASON = (
        (MISLEADING, _('Misleading content')),
        (ILLEGAL, _("Discusses/insights illegal activity")),
        (FRAUD, _("This information is false")),
        (VIOLENT, _("This content insights violence")),
        (HATE_SPEECH, _("Hate speech")),
        (HARASSMENT, _("Bullying or Harassment")),
        (OTHER, _('Other...')),
    )
    reason = models.PositiveSmallIntegerField(choices=REASON, default=MISLEADING)
    description = models.CharField(max_length=127, blank=True)
    investigated = models.BooleanField(default=False)
    removed = models.BooleanField(default=False)

    def __str__(self):
        return self.id


class Comment(models.Model):
    """ This class holds the details about the Comment table in the database.

        A Comment instance represents a comment posted on a post.
        Fields:
        user: User(FK): user that comments
        date: comment date posted
        post: Post(FK): post on which a comment has been posted
        content: what the comment says
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.user.username


class PostTag(models.Model):
    """This class holds the details about the PostTag table in the database.

        A PostTag instance maps a topic to a post, defining the subject of
        the post.
        post: Post (FK): The post the is being tagged.
        topic: Topic (FK): The topic this post is about."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'topic',)

    def __str__(self):
        return self.topic.title + ' ' + self.post.title
