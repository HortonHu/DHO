# -*- coding:utf-8 -*-


from django.conf.urls import patterns, include, url

urlpatterns = [
    url(r'^staff/', 'west.views.staff'),
    url(r'^templay/', 'west.views.templay'),
    url(r'^investigate/', 'west.views.investigate'),
]