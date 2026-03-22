# File: admin.py
# Author: Nicholas Sima (nicksima@bu.edu)
# Description: register voter_analytics models with the Django admin site

from django.contrib import admin
from .models import Voter

# Register your models here.
admin.site.register(Voter)
