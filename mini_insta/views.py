from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from .models import Profile
import random 

# Create your views here.

class ShowAllView(ListView):
    '''Define a view to show all profiles'''

    model = Profile
    
class ProfileListView(ListView):
    '''Define a view to list profiles'''

    model = Profile 
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles'

class ProfileDetailView(DetailView):
    '''Define a view to show one profile'''

    model = Profile 
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'