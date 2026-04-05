# File: views.py
# Author: Nicholas Sima (nicksima@bu.edu)
# Description: file to define both webapp and api level views

from django.views.generic import ListView, DetailView, TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Joke, Picture
from .serializers import JokeSerializer, PictureSerializer
import random


# webapp views

class RandomView(TemplateView):
    '''Show one random Joke and one random Picture'''

    template_name = 'dadjokes/random.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['joke'] = random.choice(Joke.objects.all())
        context['picture'] = random.choice(Picture.objects.all())
        return context


class JokeListView(ListView):
    '''Show all Jokes (no pictures)'''

    model = Joke
    template_name = 'dadjokes/jokes.html'
    context_object_name = 'jokes'


class JokeDetailView(DetailView):
    '''Show one Joke by primary key'''

    model = Joke
    template_name = 'dadjokes/joke.html'
    context_object_name = 'joke'


class PictureListView(ListView):
    '''Show all Pictures (no jokes)'''

    model = Picture
    template_name = 'dadjokes/pictures.html'
    context_object_name = 'pictures'


class PictureDetailView(DetailView):
    '''Show one Picture by primary key'''

    model = Picture
    template_name = 'dadjokes/picture.html'
    context_object_name = 'picture'


# REST API views

class RandomJokeAPIView(APIView):
    '''Return one random Joke as JSON (GET)'''

    def get(self, request):
        joke = random.choice(Joke.objects.all())
        return Response(JokeSerializer(joke).data)


class JokeListAPIView(APIView):
    '''Return all Jokes as JSON (GET), or create a new Joke (POST)'''

    def get(self, request):
        jokes = Joke.objects.all()
        return Response(JokeSerializer(jokes, many=True).data)

    def post(self, request):
        serializer = JokeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JokeDetailAPIView(APIView):
    '''Return one Joke by primary key as JSON (GET)'''

    def get(self, request, pk):
        joke = Joke.objects.get(pk=pk)
        return Response(JokeSerializer(joke).data)


class PictureListAPIView(APIView):
    '''Return all Pictures as JSON (GET)'''

    def get(self, request):
        pictures = Picture.objects.all()
        return Response(PictureSerializer(pictures, many=True).data)


class PictureDetailAPIView(APIView):
    '''Return one Picture by primary key as JSON (GET)'''

    def get(self, request, pk):
        picture = Picture.objects.get(pk=pk)
        return Response(PictureSerializer(picture).data)


class RandomPictureAPIView(APIView):
    '''Return one random Picture as JSON (GET)'''

    def get(self, request):
        picture = random.choice(Picture.objects.all())
        return Response(PictureSerializer(picture).data)
