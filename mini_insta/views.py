# File: views.py
# Author: Nicholas Sima (nicksima@bu.edu)
# Description: file to define views for each url


from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from .models import Profile, Post, Photo
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm
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

class ShowFollowersDetailView(DetailView):
    '''A view to show the followers of a profile'''

    model = Profile
    template_name = 'mini_insta/show_followers.html'
    context_object_name = 'profile'

class ShowFollowingDetailView(DetailView):
    '''A view to show the profiles that a profile is following'''

    model = Profile
    template_name = 'mini_insta/show_following.html'
    context_object_name = 'profile'

class UpdateProfileView(UpdateView):
    '''A view to handle updating an existing Profile'''

    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'

class DeletePostView(DeleteView):
    '''A view to handle deletion of a Post'''

    model = Post
    template_name = 'mini_insta/delete_post_form.html'

    def get_context_data(self, **kwargs):
        '''Add post and profile to the context data.'''

        context = super().get_context_data(**kwargs)
        context['post'] = self.object
        context['profile'] = self.object.profile
        return context

    def get_success_url(self):
        '''Redirect to the profile page after deleting the post.'''

        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

class UpdatePostView(UpdateView):
    '''A view to handle updating an existing Post'''

    model = Post
    form_class = UpdatePostForm
    template_name = 'mini_insta/update_post_form.html'

class SearchView(ListView):
    '''A view to handle searching profiles and posts'''

    template_name = 'mini_insta/search_results.html'
    context_object_name = 'posts'

    def dispatch(self, request, *args, **kwargs):
        '''Handle the request; return search form if no query is present.'''

        if 'query' not in request.GET:
            profile = Profile.objects.get(pk=self.kwargs['pk'])
            return render(request, 'mini_insta/search.html', {'profile': profile})
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        '''Return Posts whose caption contains the query.'''

        query = self.request.GET.get('query', '')
        return Post.objects.filter(caption__icontains=query)

    def get_context_data(self, **kwargs):
        '''Add profile, query, posts, and matching profiles to context.'''

        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query', '')
        context['profile'] = Profile.objects.get(pk=self.kwargs['pk'])
        context['query'] = query
        context['posts'] = self.get_queryset()
        context['profiles'] = Profile.objects.filter(
            username__icontains=query
        ) | Profile.objects.filter(
            display_name__icontains=query
        ) | Profile.objects.filter(
            bio_text__icontains=query
        )
        return context

class PostFeedListView(ListView):
    '''A view to show the post feed for a profile'''

    model = Post
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'posts'

    def get_queryset(self):
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        return profile.get_post_feed()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(pk=self.kwargs['pk'])
        return context

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

        # image_url = self.request.POST.get('image_url', '')
        # if image_url:
        #     Photo.objects.create(post=self.object, image_url=image_url)

        files = self.request.FILES.getlist('files')
        for f in files:
            Photo.objects.create(post=self.object, image_file=f)

        return sm