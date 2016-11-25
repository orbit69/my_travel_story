from django.conf.urls import url
from my_travel_story import views


urlpatterns = [
    url(r'^$', views.user_login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^index/$', views.index, name='index'),
    url(r'^logout/$', views.logout, name='logout')
]