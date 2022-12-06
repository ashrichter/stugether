from bootstrap_modal_forms.generic import BSModalCreateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from apps.core.models import User, Topic
from apps.feed.forms import ReportForm, PostTagForm
from apps.feed.models import Post, Vote, PostTag
from apps.notification.untilities import overloaded_create_notification


class Feed(ListView):
    """
    The feed with all posts
    """
    model = Post
    template_name = 'feed/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4

    def get_context_data(self, *args, **kwargs):
        context = super(ListView, self).get_context_data(*args, **kwargs)
        context['active'] = 'home'
        return context


class TopicFeed(ListView):
    """
    The feed with all posts that is tagged with a specific topic
    """
    model = Post
    template_name = 'feed/topic_feed.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

    def get_queryset(self):
        topic = self.kwargs['topic']
        tags = PostTag.objects.filter(topic_id=topic)
        posts = []
        for tag in tags:
            posts += [Post.objects.filter(id=tag.post_id).first()]
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic = Topic.objects.filter(id=self.kwargs['topic']).first()
        context['topic'] = topic
        return context


class ExpandPost(DetailView):
    """
    Expansion of the post with more details
    """
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tags = PostTag.objects.filter(post_id=self.kwargs['pk'])
        topics = []
        for tag in tags:
            topic = Topic.objects.filter(id=tag.topic_id).first()
            topics += [topic]
        context['tags'] = topics
        return context


class CreatePost(CreateView):
    """
    View when a post is being created.
    """
    model = Post
    fields = ['title', 'content', 'attachment']

    def form_valid(self, form):
        """ check whether the form is valid or not.

        :param form: post form
        :return: Post form validation
        """
        form.instance.author = self.request.user
        self.request.user.contribution_counter += 1
        self.request.user.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-tags', kwargs={'pk': self.object.pk})


class UpdatePost(UpdateView):
    """
    Displays update post page.
    """
    model = Post
    fields = ['title', 'content', 'attachment']

    def form_valid(self, form):
        """ check whether the form is valid or not.

        :param form: post form
        :return: Post form validation
        """
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """ check the user is original post.

        :return: user form validation
        """
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_object(self, *args, **kwargs):
        obj = super(UpdatePost, self).get_object(*args, **kwargs)
        if not obj.author == self.request.user:
            return reverse('home')
        return obj

    def get_success_url(self):
        return reverse('post-tags', kwargs={'pk': self.object.pk})


class DeletePost(UserPassesTestMixin, DeleteView):
    """
    Deleting post confirmation view.
    """
    model = Post
    success_url = '/'

    def test_func(self):
        """ check the user is original post.

        :return: user form validation
        """
        post = self.get_object()
        return post.author == self.request.user


def vote_up(request, id):
    """ Vote management system for a thumbs up(like).

    :param request,id
    :return: thumbs_up
    """
    post = Post.objects.get(id=id)
    response_data = {'up': post.up_votes,
                     'down': post.down_votes}
    if not request.user.is_authenticated:
        return JsonResponse(response_data)
    num_votes = Vote.objects.filter(user=request.user, post=post, type=2).count()
    if num_votes == 0:
        Vote.objects.create(user=request.user, post=post, type=2)
        post.up_votes += 1
        overloaded_create_notification(request, post.author, 'react', post)
    else:
        Vote.objects.filter(user=request.user, post=post, type=2).delete()
        post.up_votes -= 1
    post.save()
    response_data = {'up': post.up_votes,
                     'down': post.down_votes}
    return JsonResponse(response_data)


def vote_down(request, id):
    """ Vote management system for a thumbs downs(dislike).

   :param request,id
   :return: thumbs_down
   """
    post = Post.objects.get(id=id)
    response_data = {'up': post.up_votes,
                     'down': post.down_votes}
    if not request.user.is_authenticated:
        return JsonResponse(response_data)

    num_votes = Vote.objects.filter(user=request.user, post=post, type=1).count()
    if num_votes == 0:
        Vote.objects.create(user=request.user, post=post, type=1)
        post.down_votes += 1
        overloaded_create_notification(request, post.author, 'react', post)
    else:
        Vote.objects.filter(user=request.user, post=post, type=1).delete()
        post.down_votes -= 1
    post.save()
    response_data = {'up': post.up_votes,
                     'down': post.down_votes}
    return JsonResponse(response_data)


class ReportPostView(BSModalCreateView):
    """
    Report view, uses bootsrap modal view.
    """
    template_name = 'feed/report_post.html'
    form_class = ReportForm
    success_message = 'Success: Report submitted.'
    success_url = '/'

    def get_initial(self):
        """ Sends report to the database and reporter.

       :return: dictionary of posts and reporter
       """
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return {
            'post': post,
            'reporter': self.request.user,
        }


def search(request):
    """ Searches given query and displays it on the search page.

    :param request: http request
    :return: search page
    """
    query = request.GET.get('query', '')

    if len(query) > 0:
        users = User.objects.filter(username__contains=query) | \
                User.objects.filter(first_name__contains=query) | \
                User.objects.filter(last_name__contains=query)
        posts = Post.objects.filter(title__contains=query)
        topics = Topic.objects.filter(title__contains=query)
    else:
        users = []
        posts = []
        topics = []

    context = {
        'query': query,
        'users': users,
        'posts': posts,
        'topics': topics,
        'title': 'Search',
        'active': 'search'
    }
    return render(request, 'feed/search.html', context)


def post_tags_view(request, pk):
    """ Tag select part of edit post view is displayed.

    :param request,id
    :return: JSonResponse
    """
    json = {}
    if not request.user.is_authenticated:
        return reverse('home')
    post = Post.objects.get(id=pk)
    if not (post and post.author == request.user):
        return reverse('home')
    form = PostTagForm(initial={'post': post, })
    if request.method == "POST" and request.is_ajax():
        form = PostTagForm(request.POST)
        if form.is_valid():
            form.save()
            tags = PostTag.objects.filter(post=post).all()
            ids = []
            topics = []
            for tag in tags:
                ids += [tag.id]
                topic = Topic.objects.filter(id=tag.topic_id).first()
                topics += [topic.title]

            # handle linked post counter for each topic -> used for ranking topics
            selected_topic = Topic.objects.get(id=request.POST.get("topic"))
            selected_topic.amount_of_posts_linked += 1
            selected_topic.save()

            json['topics'] = topics
            json['ids'] = ids
            return JsonResponse(json)
        else:
            response = JsonResponse({"error": "Invalid Tag"})
            response.status_code = 400
            return response
    tags = PostTag.objects.filter(post=post).all()
    json['tags'] = tags

    context = {
        'post': post,
        'user': request.user,
        'form': form,
        'tags': tags,
    }
    return render(request, 'feed/post_tags.html', context)


def delete_tag(request, pk):
    """ Delete a tag from a post.

    :param request,id
    :return: JSonResponse to delete tag
    """
    if not request.user.is_authenticated:
        return reverse('home')
    tag = PostTag.objects.filter(id=pk).first()
    if not tag or tag.post.author != request.user:
        return reverse('home')
    # handle linked post counter for each topic -> used for ranking topics
    selected_topic = Topic.objects.get(id=tag.topic_id)
    selected_topic.amount_of_posts_linked -= 1
    selected_topic.save()
    tag.delete()
    return JsonResponse({})
