from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Picture(models.Model):
    photo = models.ImageField(upload_to='place_images')
    title = models.CharField(max_length=128, blank=True)
    description = models.TextField(blank=True)
    views = models.IntegerField(default=0)
    date = models.DateField()


class Place(models.Model):
    name = models.CharField(max_length=128)
    #koordynaty dodamy jak dowiemy sie w jaki sposob oblusugje sie google maps
    #description = models.CharField(required=False) zalezy jak dalej to przemyslimy
    description = models.TextField(blank=True)
    picture = models.ForeignKey(Picture, blank=True)
    #troche slabe zeby intem okreslac to na ile sie podobalo, od 0 do 5
    rate = models.IntegerField()



class UserProfile(models.Model):
    #odsylam do https://docs.djangoproject.com/en/1.10/ref/contrib/auth/
    user = models.OneToOneField(User)
    #opcjonalne zdjecie profilowe
    picture = models.ImageField(upload_to='profile_images', blank=True)
    place = models.ForeignKey(Place)

    def __str__(self):
        return self.user.username

    def __unicode__(self):
        #starsze wersje obsluguja unicode zamiast str
        return self.user.username