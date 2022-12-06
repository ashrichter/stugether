import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import Comment, Post
from ..notification.untilities import overloaded_create_notification


@login_required
def api_add_comment(request):
    """ Function to create new comment from JSon data

    :param request: http request
    :return: JSonResponse:success
    """
    data = json.loads(request.body)
    body = data['body']
    post_id = data['post_id']

    Comment.objects.create(post=Post.objects.get(id=post_id), body=body, user=request.user)
    overloaded_create_notification(request, Post.objects.get(id=post_id).author, 'comment', Post.objects.get(id=post_id))

    return JsonResponse({'success': True})
