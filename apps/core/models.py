from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Topic(models.Model):
    """ This class holds the details about the Topic table in the database.

        A Topic instance represents a subject/interest that can be posted
        about and can be linked to both users and academics.
        Fields:
        title: Char(127): The name of the topic
        description: Char(255): A brief description of what the topic is
        type: #Char(2): This represents the type of topic this is, with the
        options detailed below."""
    title = models.CharField(max_length=127, unique=True)
    description = models.CharField(max_length=255, blank=True)
    INSTITUTION = 'IN'
    SUBJECT = 'SB'
    MODULE = 'MD'
    SOCIETY = 'SO'
    TYPES = [
        (INSTITUTION, 'Institution'),
        (SUBJECT, 'Subject'),
        (MODULE, 'Module'),
        (SOCIETY, 'Society'),
    ]
    type = models.CharField(
        max_length=2,
        choices=TYPES,
        default=SUBJECT)
    created_at = models.DateTimeField(auto_now_add=True)
    amount_of_posts_linked = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Institution(models.Model):
    """ This class holds the details about the Institution table in the database.

        An Institution instance represents a university or college, it links
        to it's Topic instance and provides extra details.
        Fields:
        topic: Topic (FK): the topic this institution is held in."""
    topic = models.OneToOneField(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return self.topic.title


class Subject(models.Model):
    """ This class holds the details about the Course table in the database.

        A Course instance represents a course that can be studied at a
        university or college, it links to it's Topic instance and provides
        extra course-specific details.
        Fields:
        topic: Topic (FK): the topic this institution is held in."""
    topic = models.OneToOneField(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return self.topic.title


class User(AbstractUser):
    """ This class holds the details about the modified django User table in the database.

       A User instance represents a user that can have certain permissions depending whether
       they're a student, academic, admin or visitor. Also they can select their status.
       Fields:
       type: type of user
       date_of_birth: date of birth of the user
       institution: Institution in which the user is enrolled
       field_of_study: Course that the user belongs to
       bio: short biography of the user"""
    ADMIN = 1
    STUDENT = 2
    ACADEMIC = 3
    VISITOR = 4
    TYPE = (
        (ADMIN, _('Administrator')),
        (STUDENT, _('Student')),
        (ACADEMIC, _('Academic')),
        (VISITOR, _('Support Network'))
    )
    # [STUDENT, ACADEMIC]
    type = models.PositiveSmallIntegerField(choices=TYPE, default=STUDENT)
    date_of_birth = models.DateField(_('date_of_birth'), default=timezone.now)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, null=True, blank=True)
    field_of_study = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    bio = models.CharField(max_length=127, default="", blank=True)
    NONE = 1
    AWAY = 2
    IN_CLASS = 3
    FREE = 4
    STUDYING = 5
    STATUS = (
        (NONE, _('')),
        (AWAY, _('Away')),
        (IN_CLASS, _('In class')),
        (FREE, _('Free to chat')),
        (STUDYING, _('Busy studying')),
    )

    status = models.PositiveSmallIntegerField(choices=STATUS, default=NONE)
    contribution_counter = models.PositiveIntegerField(default=0)
    profile_image = models.ImageField(null=True, blank=True, upload_to='images', default='default/default.jpg')
    PRIVATE = 'private'
    PUBLIC = 'public'
    SHOW_FRIENDS = 'show_friends'
    WELL_BEING_VISIBILITY = (
        (PRIVATE, 'Private'),
        (PUBLIC, 'Public'),
        (SHOW_FRIENDS, 'Show friends'),
    )
    well_being_visibility = models.CharField(max_length=20, choices=WELL_BEING_VISIBILITY, default=PRIVATE)
    REQUIRED_FIELDS = ['type']

    def __str__(self):
        return self.username

    def is_student(self):
        return self.type == 2

    def is_academic(self):
        return self.type == 3


class Friend(models.Model):
    """ This class holds the details about a Friend request in the database.

       A Friend is a sender or a receiver and can accept or reject
       an invitation from another user.
       Fields:
       sender: User (FK): A user that sends a friend request
       receiver: User (FK): A user that receives a friend request
       accepted: Answer of the receiving user for the friend request"""
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return "Friend " + str(self.id)

    def is_accepted(self):
        return self.accepted


class Interest(models.Model):
    """ This class holds the details about the Interest table in the database.

        An Interest instance maps a user to a topic they are interested in.
        Fields:
        user: User (FK): The user that is interested in this topic.
        topic: Topic (FK): The topic that this user is interested in."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return self.topic.title + " - " + self.user.username

