from apps.core.models import Topic


def get_topics_in_ranked_order(request):
    """ Returns query of topics in order of popularity.

    :return: query of 7 topics
    """
    topics = Topic.objects.order_by('-amount_of_posts_linked')[:8]
    if request.user.is_authenticated:
        return {'top_topics': topics}
    else:
        return {'top_topics': topics}
