from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.user_login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^index/$', views.index, name='index'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^index/add_place/$', views.add_place, name='add_place'),
    url(r'^index/show_place/$', views.show_place, name='show_place'),
    url(r'^index/distance/$', views.measure_distance, name='measure_distance'),
    url(r'^shared_link*.',views.shared_link,name='shared_link')
]
