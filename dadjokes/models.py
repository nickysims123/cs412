# File: models.py
# Author: Nicholas Sima (nicksima@bu.edu)
# Description: models file to define Joke and Picture models

from django.db import models


class Joke(models.Model):
    '''Stores a dad joke with its contributor and creation timestamp.'''

    text = models.TextField()
    contributor = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Joke by {self.contributor}: {self.text[:50]}'


class Picture(models.Model):
    '''Stores a silly image/GIF URL with its contributor and creation timestamp.'''

    image_url = models.URLField()
    contributor = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Picture by {self.contributor}: {self.image_url[:50]}'
