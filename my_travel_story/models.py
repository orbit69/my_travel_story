from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    #odsylam do https://docs.djangoproject.com/en/1.10/ref/contrib/auth/
    user = models.OneToOneField(User)
    #opcjonalne zdjecie profilowe
    picture = models.ImageField(upload_to='my_travel_story/static/profile_images', blank=True,
                                default='my_travel_story/static/profile_images/no_image.png')

    def __str__(self):
        return self.user.username

    def __unicode__(self):
        #starsze wersje obsluguja unicode zamiast str
        return self.user.username


class Place(models.Model):
    name = models.CharField(max_length=128, default="nazwa")
    arrival = models.DateField(blank=True)
    departure = models.DateField(blank=True)
    latitude = models.FloatField(blank=True)
    longtitude = models.FloatField(blank=True)
    description = models.TextField(blank=True)
    user_profile_fk = models.ForeignKey(UserProfile, blank=True, null=True)


class Picture(models.Model):
    photo = models.ImageField(upload_to='my_travel_story/static/place_images',blank=True)
    title = models.CharField(max_length=128, blank=True)
    description = models.TextField(blank=True)
    rate = models.IntegerField(blank=True)
    place = models.ForeignKey(Place, blank=True)