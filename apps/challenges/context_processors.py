from apps.core.models import User


def get_users_in_ranked_order_preview(request):
    """ Returns query of users in order of their contributions Returns only 6.

    :return: query of 6 users
    """
    users = User.objects.order_by('-contribution_counter')[:6]
    if request.user.is_authenticated:
        return {'leaderboard': users}
    else:
        return {'leaderboard': users}
