# File: urls.py
# Author: Nicholas Sima (nicksima@bu.edu)
# Description: file to redirect all mini_insta urls to respective views


from django.urls import path
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


urlpatterns = [
    path('', ProfileListView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name="show_profile"),
    path('post/<int:pk>', PostDetailView.as_view(), name="show_post"),
    path('profile/<int:pk>/create_post', CreatePostView.as_view(), name="create_post"),
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name="update_profile"),
    path('post/<int:pk>/delete', DeletePostView.as_view(), name="delete_post"),
    path('post/<int:pk>/update', UpdatePostView.as_view(), name="update_post"),
    path('profile/<int:pk>/followers', ShowFollowersDetailView.as_view(), name="show_followers"),
    path('profile/<int:pk>/following', ShowFollowingDetailView.as_view(), name="show_following"),
    path('profile/<int:pk>/feed', PostFeedListView.as_view(), name="show_feed"),
    path('profile/<int:pk>/search', SearchView.as_view(), name="search"),
]