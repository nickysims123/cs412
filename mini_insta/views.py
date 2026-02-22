# File: views.py
# Author: Nicholas Sima (nicksima@bu.edu)
# Description: file to define views for each url


from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView, CreateView
from .models import Profile, Post, Photo
from .forms import CreatePostForm
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

class PostDetailView(DetailView):
    '''Define a view to show a single post'''

    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'

class CreatePostView(CreateView):
    '''A view to handle creation of a new Post'''

    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'

    def get_context_data(self, **kwargs):
        '''Add the profile to the context data.'''

        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile
        return context

    def form_valid(self, form):
        '''Attach the profile to the post before saving, and create a Photo.'''

        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile
        sm = super().form_valid(form)

        # create a Photo for this post using the image_url from the form
        image_url = self.request.POST.get('image_url', '')
        if image_url:
            Photo.objects.create(post=self.object, image_url=image_url)

        return sm