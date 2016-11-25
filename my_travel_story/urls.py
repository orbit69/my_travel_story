from django.conf.urls import url
from my_travel_story import views


urlpatterns = [
    url(r'^$', views.user_login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^index/$', views.index, name='index'),
    url(r'^restricted/$', views.restricted, name='restricted'),
    url(r'^logout/$', views.user_logout, name='logout'),
]