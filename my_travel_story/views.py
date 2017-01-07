from django.shortcuts import render
from django.db.models import Q,QuerySet
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.sessions import middleware
from django.core import serializers
from .models import *
from math import sin, cos, radians, degrees, acos


from my_travel_story.forms import UserForm, UserProfileForm, AddPlacePictureForm


def index(request):
    user_login = {'login': request.session['login']}
    coordinates = ""
    address = ""
    date = ""
    picture_path = \
    UserProfile.objects.get(id=User.objects.get(username=user_login['login']).id).picture.name.split('/')[-1]
    picture_path = picture_path.encode('ascii', 'ignore')

    user_login['name'] = User.objects.get(username=user_login['login']).first_name
    user_login['last_name'] = User.objects.get(username=user_login['login']).last_name
    user_login['avatar'] = picture_path

    queries = {
        'request_content': user_login,
    }

    if request.method == 'POST' and request.POST.get("latLng")!=None:
        coordinates = request.POST.get("latLng")
        address = request.POST.get("placeName")

    if request.method == 'POST' and request.POST.get("action")=='1':
        places = Place.objects.filter(user_profile_fk=
                                       UserProfile.objects.get(id=User.objects.get(username=user_login['login']).id))
        data = serializers.serialize("json",places)
        return HttpResponse(data)

    if request.method == 'POST' and request.POST.get('name')!=None:
        address = request.POST.get("name")
        date = request.POST.get('date').split('-')
        print address," ",date
        date = map(lambda x: datetime.strptime(x,'%b. %d, %Y')
                   ,date)
        date = map(lambda x: x.date().isoformat()
                   , date)

    if request.method == 'POST' and request.POST.get('from')!=None:
        dateFrom = request.POST.get("from")
        dateFrom = datetime.strptime(dateFrom,'%Y-%m-%d').date().isoformat()
        dateTo = request.POST.get("to")
        dateTo = datetime.strptime(dateTo, '%Y-%m-%d').date().isoformat()

        data_string = user_login['login']+"%"+user_login['name']+"%"+user_login['last_name']+"%"+str(dateFrom)+"%"+str(dateTo)

        return HttpResponse(data_string)



    if request.method == 'POST' and request.POST.get('mapName')!=None:
        address = request.POST.get("mapName")
        date = request.POST.get("mapDate").split(' - ')
        date = map(lambda x: datetime.strptime(x, '%Y-%m-%d')
                   , date)
        date = map(lambda x: x.date().isoformat()
                    , date)

    request.session['latLng'] = coordinates
    request.session['placeName'] = address
    request.session['date'] = str(date)

    user_places = Place.objects.filter(user_profile_fk=
                                       UserProfile.objects.get(id=User.objects.get(username=user_login['login']).id))
    queries['places'] = user_places

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


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def add_place(request):
    if request.method == 'POST':
        coordinates = request.session['latLng']
        address = request.session['placeName']
        lat = float(coordinates.split(",")[0][1:])
        long = float(coordinates.split(",")[1][0:-2])

        place = Place()
        place.name = address
        place.latitude = lat
        place.longtitude = long
        place.arrival = request.POST.get('place_arrival')
        place.departure = request.POST.get('place_departure')
        place.description = request.POST.get('place_story')
        place.user_profile_fk = UserProfile.objects.get(id=User.objects.get(username=request.session['login']).id)

        place.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request,'add_place.html')


def measure_distance(request):
    if request.method == "POST":
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

    else:
        return render(request, 'distance.html')


def show_place(request):
    name = request.session['placeName']
    dates = request.session['date']
    arrival = dates.split("', '")[0][2:]
    depart = dates.split("', '")[1][0:-2]
    place = Place.objects.get(name=name, arrival=arrival, departure=depart)

    pictures = Picture.objects.filter(place=place)

    if request.method == 'POST':
        picture_form = AddPlacePictureForm(request.POST, request.FILES)
        print request.FILES.keys()
        print request.POST.get.__str__()

        if picture_form.is_valid():
            picture = picture_form.save(commit=False)

            picture.place = place

            picture.save()
        else:
            print(picture_form.errors)
    else:
        picture_form = AddPlacePictureForm()

    queries = {}
    queries['place'] = place
    queries['picture_form'] = picture_form

    queries['pictures'] = map(lambda x: {'full':x, 'name': x.photo.name.split('/')[-1]}
                            ,pictures)
    print queries['pictures']

    return render(request,'show_place.html',queries)

def shared_link(request):
    queries = {}

    if request.method=='GET':
        data = request.GET.get('data')
        data = data.split('%')
        data[2] = data[2].split(" ")

        l = data[0]
        n = data[1]
        s = data[2][0]
        f = data[2][1]
        f = f.encode('ascii','ignore')
        f = datetime.date(datetime.strptime(f,'%y-%m-%d'))
        t = data[2][2]
        t = t.encode('ascii','ignore')
        t = datetime.date(datetime.strptime(t,'%y-%m-%d'))

        person = User.objects.get(username=l,first_name=n,last_name=s)
        person = UserProfile.objects.get(user=person)
        places = Place.objects.filter(user_profile_fk=person)
        places = places.filter(Q(arrival__range=(f,t)) | Q(departure__range=(f,t)))

        queries['login'] = l
        queries['name'] = n
        queries['last'] = s
        queries['fromD'] = f
        queries['toD'] = t
        queries['places'] = serializers.serialize("json", places)

    return render(request,'shared_link.html',queries)

def measure_distance(request):
    queries = {'login' : request.session['login']}
    user_places = Place.objects.filter(user_profile_fk=
                                       UserProfile.objects.get(id=User.objects.get(username=queries['login']).id)).order_by('arrival')
    if request.method == "POST":
        start_date  = datetime.strptime(request.POST.get('start_date'), "%Y-%m-%d")
        end_date    = datetime.strptime(request.POST.get('end_date'), "%Y-%m-%d")
        events = user_places.filter(arrival__range=(start_date, end_date))

        long = user_places.filter(arrival__range=(start_date, end_date)).values_list("longtitude", flat=True)
        lat = user_places.filter(arrival__range=(start_date, end_date)).values_list("latitude", flat=True)
        res_in_metres = 0.0

        if long.count() >= 2:
            for i in range(0, long.count()-1, 1):
                lat_a = radians(lat[i])
                lat_b = radians(lat[i+1])
                long_delta = radians(long[i] - long[i+1])
                distance = (sin(lat_a) * sin(lat_b) + cos(lat_a) * cos(lat_b) * cos(long_delta))
                res_in_metres += degrees(acos(distance)) * 111189.57696000072

        queries['distance'] = res_in_metres
        queries['places'] = events
    else:
        queries['places'] = user_places

    return render(request, 'distance.html', queries)
