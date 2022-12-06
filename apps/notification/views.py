from django.shortcuts import render, redirect

from apps.notification.models import Notification


def notifications(request):
    """ Displays notifications page

    If logged in then display notifications page, otherwise redirect to login page. If 'goto'
    is empty then redirect to the appropriate page.
    Types of notifications: friend request, message, react, comment and mention

    :param request: http request
    :return: notifications page
    """
    if not request.user.is_authenticated:
        return redirect('login')

    goto = request.GET.get('goto', '')
    notification_id = request.GET.get('notification', 0)

    if goto != '':
        notification = Notification.objects.get(pk=notification_id)
        notification.is_read = True
        notification.save()

        if notification.notification_type == Notification.MESSAGE:
            return redirect('conversation', user_id=notification.created_by.id)
        elif notification.notification_type == Notification.FRIEND:
            notification.is_read = False
            notification.save()
            return redirect('profile_view', username=notification.created_by.username)
        elif notification.notification_type == Notification.REACT:
            return redirect('post-detail', notification.post.id)
        elif notification.notification_type == Notification.COMMENT:
            return redirect('post-detail', notification.post.id)
        elif notification.notification_type == Notification.MENTION:
            return redirect('profile_view', username=notification.created_by.username)

    context = {'title': 'Notifications',
               'active': 'notifications',
               }
    return render(request, 'notification/notifications.html', context)
