from django.conf.urls import url
from lists import views

 
urlpatterns = [
    url(r'^$', views.homePage, name='homePage'),
    url(r'^(?P<listID>[0-9]+)/$', views.viewList, name='viewList'),
    url(r'^new/$', views.newList, name='newList'),
]