from django.conf.urls import url

from visits import views


urlpatterns = [
    url(r'^$', views.visits, name='visits')
]