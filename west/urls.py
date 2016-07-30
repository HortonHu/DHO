# -*- coding:utf-8 -*-


from django.conf.urls import patterns, include, url
from . import views

urlpatterns = [
    url(r'^staff/', views.staff),
    url(r'^templay/', views.templay),
    url(r'^investigate/', views.investigate),
]