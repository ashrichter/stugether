from apps.notification.models import Notification


def no_of_notifications(username):
    """ Returns number of notifications

    :param username: username of the person you want to get notifications for
    :return: number of notifications
    """
    counter = 0
    notification_list = Notification.objects.filter(to_user=username, is_read=False)
    for _ in notification_list:
        counter += 1
    return counter


def notifications(request):
    """ This can be accessed from all templates

    :param request: http request
    :return: notifications
    """
    if request.user.is_authenticated:
        return {'notifications': request.user.notifications.filter(is_read=False),
                'no_of_notifications': no_of_notifications(request.user)}
    else:
        return {'notifications': [],
                'no_of_notifications': 0}
