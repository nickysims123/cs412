# File: models.py
# Author: Nicholas Sima (nicksima@bu.edu)
# Description: models file to hold profile, post, and photo class definitions

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    '''Encapsulate an instagram profile'''

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.TextField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of the object'''

        return f'{self.display_name} | {self.username} --- {self.bio_text}'

    def get_absolute_url(self):
        '''Return the URL to display this profile.'''

        return reverse('show_profile', kwargs={'pk': self.pk})

    def get_all_posts(self):
        '''Return all posts for this profile, ordered by timestamp.'''

        posts = Post.objects.filter(profile=self).order_by('-timestamp')
        return posts

    def get_followers(self):
        '''Return a list of Profiles who follow this profile.'''

        return [f.follow_profile for f in Follow.objects.filter(profile=self)]

    def get_num_followers(self):
        '''Return the count of followers.'''

        return Follow.objects.filter(profile=self).count()

    def get_following(self):
        '''Return a list of Profiles that this profile follows.'''

        return [f.profile for f in Follow.objects.filter(follow_profile=self)]

    def get_num_following(self):
        '''Return the count of profiles being followed.'''

        return Follow.objects.filter(follow_profile=self).count()

    def get_post_feed(self):
        '''Return a QuerySet of Posts from followed profiles, most recent first.'''

        following = self.get_following()
        return Post.objects.filter(profile__in=following).order_by('-timestamp')

class Post(models.Model):
    '''Encapsulate an instagram post'''

    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    caption = models.TextField(blank=True)

    def __str__(self):
        '''Return a string representation of the object'''

        return f'{self.profile.display_name}: {self.caption}'

    def get_all_photos(self):
        '''Return all photos for this post.'''

        photos = Photo.objects.filter(post=self)
        return photos

    def get_all_comments(self):
        '''Return all comments for this post.'''

        return Comment.objects.filter(post=self)

    def get_likes(self):
        '''Return all likes for this post.'''

        return Like.objects.filter(post=self)

    def get_absolute_url(self):
        '''Return the URL to display this post.'''

        return reverse('show_post', kwargs={'pk': self.pk})

class Photo(models.Model):
    '''Encapsulate a photo associated with a post'''

    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank=True, upload_to='mini_insta/')
    timestamp = models.DateTimeField(auto_now=True)

    def get_image_url(self):
        '''Return the URL to the image, whether stored as a file or a URL.'''

        if self.image_file:
            return self.image_file.url
        return self.image_url

    def __str__(self):
        '''Return a string representation of the object'''

        if self.image_file:
            return f'Photo (file) for {self.post} at {self.timestamp}'
        return f'Photo (url) for {self.post} at {self.timestamp}'

class Follow(models.Model):
    '''Encapsulate a follow relationship between two Profiles'''

    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='profile')
    follow_profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='follower_profile')
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of the object'''

        return f'{self.follow_profile.display_name} follows {self.profile.display_name}'

class Comment(models.Model):
    '''Encapsulate a comment made by a Profile on a Post'''

    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    text = models.TextField(blank=True)

    def __str__(self):
        '''Return a string representation of the object'''

        return f'{self.profile.display_name} on "{self.post}": {self.text}'

class Like(models.Model):
    '''Encapsulate a like given by a Profile to a Post'''

    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of the object'''

        return f'{self.profile.display_name} likes "{self.post}"'