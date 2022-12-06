from django.db.models import Q

from apps.core.models import Friend, User, Interest


def get_list_of_friends(username):
    """ Function to get number of friends for a given user.

    :param username: username of the profile
    :return: number of friends the user has
    """
    counter = 0
    fr_list = Friend.objects.filter(Q(Q(sender=User.objects.get(username=username).id)
                                      | Q(receiver=User.objects.get(username=username).id)),
                                    Q(accepted=True))
    for _ in fr_list:
        counter += 1
    return counter


def get_list_of_topics(username):
    """ Function to get number of topics for a given user.

    :param username: username of the profile
    :return: number of topics the user follows
    """
    counter = 0
    topic_list = Interest.objects.filter(user=User.objects.get(username=username).id)
    for _ in topic_list:
        counter += 1
    return counter


def get_friend_requests(username):
    """ Returns a list of friend requests.

    :param username: username of the receiver
    :return: list of friend objects
    """
    list_of_friend_requests = Friend.objects.filter(receiver=User.objects.get(username=username).id, accepted=False)
    return list_of_friend_requests
