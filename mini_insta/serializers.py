# File: serializers.py
# Author: Nicholas Sima (nicksima@bu.edu)
# Description: serializers to allow our mini_insta REST API to talk w a react native client

from rest_framework import serializers
from .models import Profile, Post, Photo


class ProfileSerializer(serializers.ModelSerializer):
    '''Serialize profile fields.'''

    class Meta:
        model = Profile
        fields = ['id', 'username', 'display_name', 'profile_image_url', 'bio_text', 'join_date']


class PhotoSerializer(serializers.ModelSerializer):
    '''Serialize photo fields, including a resolved image URL.'''

    image = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ['id', 'image_url', 'image_file', 'image', 'timestamp']

    def get_image(self, obj):
        return obj.get_image_url()


class PostSerializer(serializers.ModelSerializer):
    '''Serialize post fields with nested photos.'''

    photos = PhotoSerializer(source='get_all_photos', many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'profile', 'caption', 'timestamp', 'photos']
        read_only_fields = ['profile', 'timestamp']
