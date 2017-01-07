from django import forms
from django.contrib.auth.models import User
from .models import Picture, Place, UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture', )


class AddPlacePictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ('photo', 'title', 'description', 'rate')


class MeasureForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('arrival', 'arrival')