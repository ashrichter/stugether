from django.shortcuts import render, redirect

from apps.challenges.utilities import get_users_in_ranked_order


def leaderboard_page(request):
    """ Displays leaderboard page

    :param request: http request
    :return: leaderboard page
    """
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        ordered_list_of_users = get_users_in_ranked_order()

        context = {'title': 'Leaderboard', 'active': 'leaderboard', 'ordered_list_of_users': ordered_list_of_users}
        return render(request, 'challenges/leaderboard.html', context)
