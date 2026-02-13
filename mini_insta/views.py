from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from .models import Profile
import random 

# Create your views here.

class ShowAllView(ListView):
    '''Define a view to show all profiles'''

    model = Profile
    