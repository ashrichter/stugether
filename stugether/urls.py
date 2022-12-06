"""stugether URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve

from apps.challenges.views import leaderboard_page
from apps.core.views import logout_user, login_page, register_page, edit_profile_page, terms_page, \
    select_topics_page, profile_page, profile_following_topics_page, friends_page, add_friend, delete_friend, \
    privacy_policy_page, AddTopicView, settings_page
from apps.feed.views import (
    Feed,
    ExpandPost,
    CreatePost,
    UpdatePost,
    DeletePost,
    vote_up,
    vote_down,
    ReportPostView,
    search,
    post_tags_view,
    delete_tag,
    TopicFeed,
)
from apps.notification.views import notifications
from apps.feed.api import api_add_comment
from apps.health.views import health_page

urlpatterns = [
    # Terms, privacy policy & cookies
    path('terms-and-conditions/', terms_page, name='terms-and-conditions'),
    path('privacy-policy/', privacy_policy_page, name='privacy-policy'),

    # Main app
    path('', Feed.as_view(), name='home'),

    # Profile
    path('profile/edit', edit_profile_page, name='edit-profile'),
    path('<username>/profile/', profile_page, name='profile_view'),
    path('<username>/following-topics/', profile_following_topics_page, name='following-topics'),
    path('<username>/friends/', friends_page, name='friends'),

    # Notifications
    path('notifications/', notifications, name='notifications'),

    # Friends Handling
    path('ajax/addFriend', add_friend, name="add_friend"),
    path('ajax/deleteFriend', delete_friend, name="delete_friend"),

    # Explore
    path('select-topics/', select_topics_page, name='select-topics'),

    # Core
    path('register/', register_page, name='register'),
    path('login/', login_page, name='login'),
    path('logout/', logout_user, name='logout'),
    path('admin/', admin.site.urls),
    path('settings/', settings_page, name='settings'),

    # Post
    path('', Feed.as_view(), name='home'),
    path('post/<int:pk>/', ExpandPost.as_view(), name='post-detail'),
    path('post/new/', CreatePost.as_view(), name='post-create'),
    path('post/<int:pk>/update/', UpdatePost.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', DeletePost.as_view(), name='post-delete'),
    path('post/<int:pk>/report/', ReportPostView.as_view(), name='post-report'),
    path('post/<int:pk>/tags/', post_tags_view, name='post-tags'),
    path('post/tag/<int:pk>/delete/', delete_tag, name='post-tag-delete'),

    # Votes
    path('post/<int:id>/vote/up', vote_up, name='vote_up'),
    path('post/<int:id>/vote/down', vote_down, name='vote_down'),

    # Topics
    path('topic/add/', AddTopicView.as_view(), name='topic-add'),
    path('topic/<slug:topic>/feed/', TopicFeed.as_view(), name='topic-feed'),

    # Search
    path('search/', search, name='search'),

    # Challenges & Leaderboard
    path('leaderboard/', leaderboard_page, name='leaderboard'),

    # Well being
    path('health/', health_page, name='health'),

    # API
    path('api/add_comment/', api_add_comment, name='api_add_comment'),

    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]

