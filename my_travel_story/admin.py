from django.contrib import admin
from .models import Picture, Place
from .models import UserProfile

admin.site.register(Picture)
admin.site.register(Place)
admin.site.register(UserProfile)