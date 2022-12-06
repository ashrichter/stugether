from .models import Notification


def create_notification(request, to_user, notification_type):
    """ Creates a notification in the database.

    :param request: http request
    :param to_user: the user the notification is for
    :param notification_type: the type of notification
    """
    if request.user != to_user:
        Notification.objects.create(to_user=to_user, notification_type=notification_type,
                                    created_by=request.user)


def overloaded_create_notification(request, to_user, notification_type, linking_post):
    """ Creates a notification in the database (function overload).

    :param linking_post: post linked to the notification
    :param request: http request
    :param to_user: the user the notification is for
    :param notification_type: the type of notification
    """
    if request.user != to_user:
        Notification.objects.create(to_user=to_user, notification_type=notification_type,
                                    created_by=request.user, post=linking_post)
