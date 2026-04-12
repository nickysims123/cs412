# File: views.py
# Author: Nicholas Sima (nicksima@bu.edu)
# Description: file to define views for each url


from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import ProfileSerializer, PostSerializer
from .models import Profile, Post, Photo, Follow, Like
from .forms import CreatePostForm, CreateProfileForm, UpdateProfileForm, UpdatePostForm
import random

# Create your views here.

class MiniInstaLoginMixin(LoginRequiredMixin):
    '''Mixin requiring login; provides helper to retrieve the logged-in user's Profile.'''

    def get_login_url(self):
        '''Return the URL of the mini_insta login page.'''
        return reverse('login')

    def get_login_profile(self):
        '''Return the Profile associated with the currently logged-in user.'''
        return Profile.objects.get(user=self.request.user)


# web app views

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                login_profile = Profile.objects.get(user=self.request.user)
                context['login_profile'] = login_profile
                context['is_following'] = Follow.objects.filter(
                    profile=self.object, follow_profile=login_profile
                ).exists()
            except Profile.DoesNotExist:
                pass
        return context

class PostDetailView(DetailView):
    '''Define a view to show a single post'''

    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                login_profile = Profile.objects.get(user=self.request.user)
                context['is_liked'] = Like.objects.filter(
                    post=self.object, profile=login_profile
                ).exists()
            except Profile.DoesNotExist:
                pass
        return context

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

class ShowOwnProfileView(MiniInstaLoginMixin, DetailView):
    '''A view to show the logged-in user's own profile'''

    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'

    def get_object(self):
        return Profile.objects.get(user=self.request.user)


class UpdateProfileView(MiniInstaLoginMixin, UpdateView):
    '''A view to handle updating an existing Profile'''

    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

class DeletePostView(MiniInstaLoginMixin, DeleteView):
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

class UpdatePostView(MiniInstaLoginMixin, UpdateView):
    '''A view to handle updating an existing Post'''

    model = Post
    form_class = UpdatePostForm
    template_name = 'mini_insta/update_post_form.html'

class SearchView(MiniInstaLoginMixin, ListView):
    '''A view to handle searching profiles and posts'''

    template_name = 'mini_insta/search_results.html'
    context_object_name = 'posts'

    def dispatch(self, request, *args, **kwargs):
        '''Handle the request; return search form if no query is present.'''

        if 'query' not in request.GET:
            profile = self.get_login_profile()
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
        context['profile'] = self.get_login_profile()
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

class PostFeedListView(MiniInstaLoginMixin, ListView):
    '''A view to show the post feed for a profile'''

    model = Post
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return self.get_login_profile().get_post_feed()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_login_profile()
        return context

class CreatePostView(MiniInstaLoginMixin, CreateView):
    '''A view to handle creation of a new Post'''

    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'

    def get_context_data(self, **kwargs):
        '''Add the profile to the context data.'''

        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_login_profile()
        return context

    def form_valid(self, form):
        '''Attach the profile to the post before saving, and create a Photo.'''

        form.instance.profile = self.get_login_profile()
        sm = super().form_valid(form)

        # image_url = self.request.POST.get('image_url', '')
        # if image_url:
        #     Photo.objects.create(post=self.object, image_url=image_url)

        files = self.request.FILES.getlist('files')
        for f in files:
            Photo.objects.create(post=self.object, image_file=f)

        return sm
    

class FollowProfileView(MiniInstaLoginMixin, View):
    '''Create a Follow relationship between the logged-in user and another Profile.'''

    def get(self, request, *args, **kwargs):
        other_profile = Profile.objects.get(pk=self.kwargs['pk'])
        login_profile = self.get_login_profile()
        Follow.objects.get_or_create(profile=other_profile, follow_profile=login_profile)
        return redirect(reverse('show_profile', kwargs={'pk': other_profile.pk}))


class DeleteFollowView(MiniInstaLoginMixin, View):
    '''Delete a Follow relationship between the logged-in user and another Profile.'''

    def get(self, request, *args, **kwargs):
        other_profile = Profile.objects.get(pk=self.kwargs['pk'])
        login_profile = self.get_login_profile()
        Follow.objects.filter(profile=other_profile, follow_profile=login_profile).delete()
        return redirect(reverse('show_profile', kwargs={'pk': other_profile.pk}))


class LikePostView(MiniInstaLoginMixin, View):
    '''Create a Like on a Post for the logged-in user.'''

    def get(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs['pk'])
        login_profile = self.get_login_profile()
        Like.objects.get_or_create(post=post, profile=login_profile)
        return redirect(reverse('show_post', kwargs={'pk': post.pk}))


class DeleteLikeView(MiniInstaLoginMixin, View):
    '''Delete a Like on a Post for the logged-in user.'''

    def get(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs['pk'])
        login_profile = self.get_login_profile()
        Like.objects.filter(post=post, profile=login_profile).delete()
        return redirect(reverse('show_post', kwargs={'pk': post.pk}))


class CreateProfileView(CreateView):
    '''A view to handle creation of a new Profile along with a new User.'''

    form_class = CreateProfileForm
    template_name = 'mini_insta/create_profile_form.html'

    def get_context_data(self, **kwargs):
        '''Add the UserCreationForm to the context.'''

        context = super().get_context_data(**kwargs)
        context['user_creation_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        '''Create the User, log them in, attach them to the Profile, then save.'''

        user_creation_form = UserCreationForm(self.request.POST)
        user = user_creation_form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        form.instance.user = user
        return super().form_valid(form)


# REST API views

@method_decorator(csrf_exempt, name='dispatch')
class ProfileListAPIView(APIView):
    '''Return all Profiles as JSON (GET).'''

    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        profiles = Profile.objects.all()
        return Response(ProfileSerializer(profiles, many=True).data)


@method_decorator(csrf_exempt, name='dispatch')
class ProfileDetailAPIView(APIView):
    '''Return one Profile by primary key as JSON (GET).'''

    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request, pk):
        profile = Profile.objects.get(pk=pk)
        return Response(ProfileSerializer(profile).data)


@method_decorator(csrf_exempt, name='dispatch')
class ProfilePostListAPIView(APIView):
    '''Return all Posts for a Profile as JSON (GET), or create a new Post (POST).'''

    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request, pk):
        profile = Profile.objects.get(pk=pk)
        posts = profile.get_all_posts()
        return Response(PostSerializer(posts, many=True).data)

    def post(self, request, pk):
        profile = Profile.objects.get(pk=pk)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(profile=profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class ProfileFeedAPIView(APIView):
    '''Return the post feed for a Profile as JSON (GET).'''

    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request, pk):
        profile = Profile.objects.get(pk=pk)
        posts = profile.get_post_feed()
        return Response(PostSerializer(posts, many=True).data)
