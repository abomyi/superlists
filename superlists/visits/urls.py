from django.conf.urls import url

from visits import views


urlpatterns = [
    url(r'^$', views.visits, name='visits'),
    url(r'^create/$', views.create, name='create'),
    url(r'^(?P<visitID>[0-9]+)/$', views.getVisit, name='getVisit'),
]