# File: models.py
# Author: Nicholas Sima (nicksima@bu.edu)
# Description: models file to hold profile, post, and photo class definitions

from django.db import models
from django.urls import reverse

# Create your models here.

class Profile(models.Model):
    '''Encapsulate an instagram profile'''

    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.TextField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of the object'''

        return f'{self.display_name} | {self.username} --- {self.bio_text}'

    def get_all_posts(self):
        '''Return all posts for this profile, ordered by timestamp.'''

        posts = Post.objects.filter(profile=self).order_by('-timestamp')
        return posts

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

    def get_absolute_url(self):
        '''Return the URL to display this post.'''

        return reverse('show_post', kwargs={'pk': self.pk})

class Photo(models.Model):
    '''Encapsulate a photo associated with a post'''

    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of the object'''

        return f'Photo for {self.post} at {self.timestamp}'