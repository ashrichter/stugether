import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.messages import get_messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from apps.core.forms import CreateUserForm, ChangeUserForm, FriendForm, TopicForm
from .models import User, Topic, Interest, Friend
from bootstrap_modal_forms.generic import BSModalCreateView
from .untilities import get_list_of_friends, get_list_of_topics
from ..feed.models import Post
from ..health.models import Health
from ..health.utilities import get_weekly_health_averages
from ..notification.models import Notification
from ..notification.untilities import create_notification


def profile_page(request, username):
    """ Displays the specified user's profile page.

    If this user is the currently logged in user, this allows them to edit
    their profile, otherwise they may add this user as a friend, or delete
    them dependent on the calculated status.
    status:
    1 = viewing unknown user
    2 = the user's own profile
    3 = friend request sent to this user
    4 = friend request received by this user
    5 = this user is your friend
    NEEDS TO BE ALTERED DEPENDENT ON PRIVACY SETTINGS OF THE USER.
    """
    if not request.user.is_authenticated:
        return redirect('home')
    user = User.objects.get(username=username)
    status = 1
    form = FriendForm(initial={'sender': request.user,
                               'receiver': user,
                               'accepted': False})
    no_of_friends = get_list_of_friends(username)
    no_of_topics = get_list_of_topics(username)
    current_week = datetime.date.today().isocalendar()[1]
    health_data = Health.objects.filter(date__week=current_week, user=user)
    weekly_averages = get_weekly_health_averages(health_data)

    user_posts = Post.objects.filter(author=user)[::-1]
    if user.id == request.user.id:
        status = 2
    else:
        if Friend.objects.filter(sender=request.user, receiver=user).exists():
            status = 3
            f = Friend.objects.get(sender=request.user, receiver=user)
            if f.is_accepted():
                status = 5
        if Friend.objects.filter(sender=user, receiver=request.user).exists():
            status = 4
            f = Friend.objects.get(sender=user, receiver=request.user)
            form = FriendForm(initial={'sender': user,
                                       'receiver': request.user,
                                       'accepted': True})
            if f.is_accepted():
                status = 5

    context = {'title': user.first_name + ' (@' + user.username + ')',
               'active': 'profile', 'user': user, 'status': status,
               'form': form, 'no_of_friends': no_of_friends,
               'no_of_topics': no_of_topics, 'user_posts': user_posts,
               'weekly_averages': weekly_averages,}

    return render(request, 'core/profile.html', context)


def edit_profile_page(request):
    """ Displays edit profile page.

    If user is not logged in, goes to home page. If POST method and form
    is valid then save and redirect to home page, otherwise just go to
    edit profile page.

    :param request: http request
    :return: home or register page
    """
    if not request.user.is_authenticated:
        return redirect('home')
    else:
        form = ChangeUserForm(instance=request.user)
        if request.method == 'POST':
            form = ChangeUserForm(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('profile_view', request.user.username)

    context = {'form': form, 'title': 'Edit Profile'}
    return render(request, 'core/profile_edit.html', context)


def register_page(request):
    """ Displays register page.

    If user is already logged in then redirected to home page. If POST method
    and the form filled is valid then save the authentication info in default
    django User and additional info to UserProfile in database.
    After redirect to login page.

    :param request: http request
    :return: register page or login page
    """
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + username)

                # add user to correct group
                user = User.objects.get(username=username)
                if user.is_student():
                    user.groups.add(Group.objects.get(name='Students'))
                elif user.is_academic:
                    user.groups.add(Group.objects.get(name='Academics'))

                return redirect('login')

        context = {'form': form, 'title': 'Register', 'active': 'register'}
        return render(request, 'core/register.html', context)


def login_page(request):
    """ Displays login page.

    If user is already logged in then redirected to home page. If POST method
    then get username, password then authenticate the user. Redirect to home
    page if valid details given, otherwise just render to login page again
    with a message.

    :param request: http request
    :return: login page or home page
    """
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or password is incorrect')
                context = {'title': 'Login'}
                return render(request, 'core/login.html', context)

        context = {'title': 'Login', 'active': 'login'}
        return render(request, 'core/login.html', context)


def logout_user(request):
    """ Logs the user out.

    Uses django built in logout function to log the current user and
    redirect to login page.

    :param request: http request
    :return: login page
    """
    logout(request)
    return redirect('login')


def terms_page(request):
    """ Displays terms of service page.

    :param request: http request
    :return: terms page
    """
    context = {'title': 'Terms and Conditions'}
    return render(request, 'core/terms_and_conditions.html', context)


def privacy_policy_page(request):
    """ Displays privacy policy page.

    :param request: http request
    :return: terms page
    """
    context = {'title': 'Privacy Policy'}
    return render(request, 'core/privacy_policy.html', context)


def select_topics_page(request):
    """ Displays select topic page and lets you choose topics to follow.

    If user is not logged in then redirected to home page. If POST method
    then adds selected topics to user's topic following. Otherwise just
    displays the select topic page.

    :param request: http request
    :return: select topic page
    """
    if not request.user.is_authenticated:
        return redirect('home')
    else:
        queryset = Topic.objects.all()
        # getting a list of topics followed the current user
        querysetInterests = Interest.objects.filter(user=request.user)
        interests = []
        for i in querysetInterests:
            interests.append(i.topic)

        context = {'title': 'Topics Selection',
                   'active': 'topic-select',
                   'object_list': queryset,
                   'interest_list': interests,
                   'is_post': False,
                   messages: get_messages(request)}

        if request.method == "POST":
            # Following
            selected_topics = request.POST.getlist('topic-choices')
            for topic in selected_topics:
                Interest.objects.create(user=request.user, topic=Topic.objects.filter(id=topic)[0])

            # Unfollowing
            selected_unfollow_topics = request.POST.getlist('topic-following')
            for topic in selected_unfollow_topics:
                Interest.objects.filter(user=request.user, topic=topic).delete()
            messages.success(request, 'Test successful')
            return HttpResponseRedirect(reverse('select-topics'))
        else:
            return render(request, 'core/select_topics.html', context)


def profile_following_topics_page(request, username):
    """ Displays a user's following topics page.

    :param username: username of the profile
    :param request: http request
    :return: follow topic page
    """
    user = User.objects.get(username=username)
    is_own = False

    if user.id == request.user.id and request.user.is_authenticated:
        is_own = True

    queryset = Interest.objects.all()

    context = {'title': 'Following Topics',
               'interest_list': queryset,
               'user': user,
               'is_own': is_own,
               }
    return render(request, 'core/profile_following_topics.html', context)


def friends_page(request, username):
    """ Displays a page of your list of friends.

    :param request: http request
    :param username: username of the user
    :return: list of friend objects
    """
    user = User.objects.get(username=username)
    queryset = Friend.objects.filter(Q(receiver=user, accepted=True) |
                                     Q(sender=user, accepted=True))
    context = {'title': 'Friends',
               'user': user,
               'friends_list': queryset
               }
    return render(request, 'core/profile_friends.html', context)


def add_friend(request):
    """ Handles an ajax request to add or accept a friend request to the database.

    :param request: http request
    :return: JSonResponse
    """
    response_data = {'title': 'error'}
    if request.method == "POST" and request.is_ajax():
        # get form data
        form = FriendForm(request.POST)
        s = request.POST.get('sender')
        r = request.POST.get('receiver')
        if Friend.objects.filter(sender=s, receiver=r).exists():
            f = Friend.objects.get(sender=s, receiver=r)
            form = FriendForm(request.POST, instance=f)
        # save the data and after fetch the object in instance
        if form.is_valid() and s != r:
            form.save()

            # creating notification if current user isn't the receiver
            if request.user != User.objects.get(id=request.POST.get('receiver')):
                create_notification(request, User.objects.get(id=request.POST.get('receiver')), 'friend')

            # accepting friend request -> remove notification
            if request.user == User.objects.get(id=request.POST.get('receiver')):
                try:
                    n = Notification.objects.get(to_user=User.objects.get(id=r), created_by=User.objects.get(id=s),
                                                 notification_type='friend')
                    n.delete()
                except ObjectDoesNotExist:
                    pass

            # send to client side.
            response_data['title'] = 'success'
            return JsonResponse(response_data)
        else:
            # some form errors occurred.
            return JsonResponse(response_data)

    # some error occurred
    return JsonResponse(response_data)


def delete_friend(request):
    """ Handles an ajax request to delete a friend request from the database.

    :param request: http request
    :return: JsonResponse
    """
    response_data = {'title': 'error'}
    if request.user.is_authenticated and request.method == "POST" and request.is_ajax():
        s = request.POST.get('sender')
        r = request.POST.get('receiver')
        if Friend.objects.filter(sender=s, receiver=r).exists():
            f = Friend.objects.get(sender=s, receiver=r)
            f.delete()
            try:
                n = Notification.objects.get(to_user=User.objects.get(id=r), created_by=User.objects.get(id=s),
                                             notification_type='friend')
                n.delete()
            except ObjectDoesNotExist:
                pass
            response_data['title'] = 'success'
            return JsonResponse(response_data)

    return JsonResponse(response_data)


class AddTopicView(BSModalCreateView):
    """
    Add topic page bootstrap model view
    """
    template_name = 'core/topic_add.html'
    form_class = TopicForm
    success_message = 'Success: Topic added.'
    success_url = reverse_lazy('home')


def settings_page(request):
    """ Displays settings page

    Goes to home page if not logged in, else goes to settings page.
    :param request: https request
    :return: settings page
    """
    context = {'title': 'Settings',
               'active': 'settings'
               }
    if not request.user.is_authenticated:
        return redirect('home')
    else:
        return render(request, 'core/settings.html', context)