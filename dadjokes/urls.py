# File: urls.py
# Author: Nicholas Sima (nicksima@bu.edu)
# Description: file to define URL endpoints main app routes to dadjokes app and API


from django.urls import path
from .views import (
    RandomView, JokeListView, JokeDetailView, PictureListView, PictureDetailView,
    RandomJokeAPIView, JokeListAPIView, JokeDetailAPIView,
    PictureListAPIView, PictureDetailAPIView, RandomPictureAPIView,
)

urlpatterns = [
    # webapp views
    path('', RandomView.as_view(), name='dadjokes_random'),
    path('random', RandomView.as_view(), name='dadjokes_random_alt'),
    path('jokes', JokeListView.as_view(), name='dadjokes_jokes'),
    path('joke/<int:pk>', JokeDetailView.as_view(), name='dadjokes_joke'),
    path('pictures', PictureListView.as_view(), name='dadjokes_pictures'),
    path('picture/<int:pk>', PictureDetailView.as_view(), name='dadjokes_picture'),

    # REST endpoints
    path('api/', RandomJokeAPIView.as_view(), name='api_random_joke'),
    path('api/random', RandomJokeAPIView.as_view(), name='api_random_joke_alt'),
    path('api/jokes', JokeListAPIView.as_view(), name='api_jokes'),
    path('api/joke/<int:pk>', JokeDetailAPIView.as_view(), name='api_joke'),
    path('api/pictures', PictureListAPIView.as_view(), name='api_pictures'),
    path('api/picture/<int:pk>', PictureDetailAPIView.as_view(), name='api_picture'),
    path('api/random_picture', RandomPictureAPIView.as_view(), name='api_random_picture'),
]
