from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# Create your views here.

def home_page(request):

    template = 'hw/home.html'

    return render(request, template)