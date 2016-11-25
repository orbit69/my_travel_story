from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from .models import *


from my_travel_story.forms import UserForm, UserProfileForm

def index(request):
    user_login = request.session['login']

    picture_path = UserProfile.objects.get(id=User.objects.get(username=user_login).id).picture.name.split('/')[-1]
    picture_path = picture_path.encode('ascii', 'ignore')

    queries = {
        'request_content': user_login,
        'picture' : picture_path,
    }

    return render(request, 'index.html', queries)

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            #zapisuje dane z form do bazy danych
            user = user_form.save()
            #haszuje haslo
            user.set_password(user.password)
            user.save()

            #nie zapisuje sie samo wiec moge ustalic czy dodaje zdjecie
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        #nie dostalismy POSTa wiec renderuje ModelForm ktore jest gotowe na
        #input od uzytkownika
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'register.html',
                  {'user_form' : user_form,
                   'profile_form' : profile_form,
                   'registered' : registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                request.session['login'] = username
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your MyTravelStory account is disabled, please contact admin.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'login.html', {})

def user_logout(request):
    del request.session['login']
    logout(request)
    return HttpResponseRedirect(reverse('login'))

