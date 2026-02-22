# File: urls.py
# Author: Nicholas Sima (nicksima@bu.edu)
# Description: file to redirect all mini_insta urls to respective views


from django.urls import path
from .views import ProfileListView
from .views import ProfileDetailView
from .views import PostDetailView
from .views import CreatePostView


urlpatterns = [
    path('', ProfileListView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name="show_profile"),
    path('post/<int:pk>', PostDetailView.as_view(), name="show_post"),
    path('profile/<int:pk>/create_post', CreatePostView.as_view(), name="create_post"),
]