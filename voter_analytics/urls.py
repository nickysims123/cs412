# File: urls.py
# Author: Nicholas Sima (nicksima@bu.edu)
# Description: urls to reroute main app to voter_analytics app



from django.urls import path
from .views import *

urlpatterns = [
    path('', VoterListView.as_view(), name='voters'),
    path('voter/<int:pk>', VoterDetailView.as_view(), name='voter'),
    path('graphs', VoterGraphView.as_view(), name='graphs'),
]
