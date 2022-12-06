from apps.core.models import User


def get_users_in_ranked_order():
    """ Returns query of users in order of their contributions.

    :return: query of users
    """
    users = User.objects.order_by('-contribution_counter')

    return users
