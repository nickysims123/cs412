from django.urls import path 
from .views import ProfileListView
from .views import ProfileDetailView


urlpatterns = [
    path('', ProfileListView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name="show_profile")
]