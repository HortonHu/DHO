# -*- coding:utf-8 -*-

from django.conf.urls import patterns, include, url

urlpatterns = [
    url(r'^login/', 'users.views.user_login'),
    url(r'^logout/', 'users.views.user_logout'),
]
