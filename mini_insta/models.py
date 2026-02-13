from django.db import models

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