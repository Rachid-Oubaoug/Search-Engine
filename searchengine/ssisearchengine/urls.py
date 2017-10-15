from django.conf.urls import url
from . import views

urlpatterns = [
    #url(r'^index/$', views.search_index),
    #url(r'^search/(\d+)$', views.search),
    url(r'^search/$', views.search),
]