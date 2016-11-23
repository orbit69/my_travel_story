from django.contrib import admin
from my_travel_story.models import Picture, Place
from my_travel_story.models import UserProfile

admin.site.register(Picture)
admin.site.register(Place)
admin.site.register(UserProfile)