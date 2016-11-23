from django.shortcuts import render
from my_travel_story.forms import UserForm, UserProfileForm


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
                  'mytravelstory.html',
                  {'user_form' : user_form,
                   'profile_form' : profile_form,
                   'registered' : registered})

