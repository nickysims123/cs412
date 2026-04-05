# File: serializers.py
# Author: Nicholas Sima (nicksima@bu.edu)
# Description: file to contain serializer definitions for Joke and Picture objects

from rest_framework import serializers
from .models import Joke, Picture


class JokeSerializer(serializers.ModelSerializer):
    '''Serialize all fields of a Joke.'''

    class Meta:
        model = Joke
        fields = ['id', 'text', 'contributor', 'created']


class PictureSerializer(serializers.ModelSerializer):
    '''Serialize all fields of a Picture.'''

    class Meta:
        model = Picture
        fields = ['id', 'image_url', 'contributor', 'created']
