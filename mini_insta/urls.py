# File: urls.py
# Author: Nicholas Sima (nicksima@bu.edu)
# Description: file to redirect all mini_insta urls to respective views


from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from .views import ProfileListView
from .views import ProfileDetailView
from .views import PostDetailView
from .views import CreatePostView
from .views import UpdateProfileView
from .views import DeletePostView
from .views import UpdatePostView
from .views import ShowFollowersDetailView
from .views import ShowFollowingDetailView
from .views import PostFeedListView
from .views import SearchView
from .views import ShowOwnProfileView
from .views import CreateProfileView
from .views import FollowProfileView, DeleteFollowView
from .views import LikePostView, DeleteLikeView
from .views import LoginAPIView, ProfileListAPIView, ProfileDetailAPIView, ProfilePostListAPIView, ProfileFeedAPIView


urlpatterns = [
    # auth
    path('login/', LoginView.as_view(template_name='mini_insta/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='logout_confirmation'), name='logout'),
    path('logout_confirmation/', TemplateView.as_view(template_name='mini_insta/logged_out.html'), name='logout_confirmation'),

    # webapp views
    path('', ProfileListView.as_view(), name="show_all_profiles"),
    path('profile', ShowOwnProfileView.as_view(), name="show_own_profile"),
    path('create_profile', CreateProfileView.as_view(), name="create_profile"),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name="show_profile"),
    path('post/<int:pk>', PostDetailView.as_view(), name="show_post"),
    path('profile/create_post', CreatePostView.as_view(), name="create_post"),
    path('profile/update', UpdateProfileView.as_view(), name="update_profile"),
    path('post/<int:pk>/delete', DeletePostView.as_view(), name="delete_post"),
    path('post/<int:pk>/update', UpdatePostView.as_view(), name="update_post"),
    path('profile/<int:pk>/follow', FollowProfileView.as_view(), name="follow_profile"),
    path('profile/<int:pk>/delete_follow', DeleteFollowView.as_view(), name="delete_follow"),
    path('post/<int:pk>/like', LikePostView.as_view(), name="like_post"),
    path('post/<int:pk>/delete_like', DeleteLikeView.as_view(), name="delete_like"),
    path('profile/<int:pk>/followers', ShowFollowersDetailView.as_view(), name="show_followers"),
    path('profile/<int:pk>/following', ShowFollowingDetailView.as_view(), name="show_following"),
    path('profile/feed', PostFeedListView.as_view(), name="show_feed"),
    path('profile/search', SearchView.as_view(), name="search"),

    # REST endpoints
    path('api/login', LoginAPIView.as_view(), name='api_login'),
    path('api/profiles', ProfileListAPIView.as_view(), name='api_profiles'),
    path('api/profile/<int:pk>', ProfileDetailAPIView.as_view(), name='api_profile'),
    path('api/profile/<int:pk>/posts', ProfilePostListAPIView.as_view(), name='api_profile_posts'),
    path('api/profile/<int:pk>/feed', ProfileFeedAPIView.as_view(), name='api_profile_feed'),

]

'''
Reading a profile or a list of profiles.

Reading posts (and pictures) for one profile.

Reading a feed for one profile (i.e., similar to the 'profile/<int:pk>/feed' URL from the web version of mini_insta)

Creating a post.


'''