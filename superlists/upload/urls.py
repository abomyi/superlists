from django.conf.urls import url
from upload import views

 
urlpatterns = [
    url(r'^signS3/$', views.signS3, name='signS3'),
    url(r'^$', views.upload, name='upload'),
]