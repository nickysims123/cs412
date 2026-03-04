# File: forms.py
# Author: Nicholas Sima (nicksima@bu.edu)
# Description: form to intake a new post



from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    '''A form to create a new Post.'''

    class Meta:
        '''associate this form with the Post model'''
        model = Post
        fields = ['caption']

class UpdateProfileForm(forms.ModelForm):
    '''A form to update an existing Profile.'''

    class Meta:
        '''associate this form with the Profile model'''
        model = Profile
        fields = ['display_name', 'profile_image_url', 'bio_text']

class UpdatePostForm(forms.ModelForm):
    '''A form to update an existing Post.'''

    class Meta:
        '''associate this form with the Post model'''
        model = Post
        fields = ['caption']
