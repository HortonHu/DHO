# -*- coding:utf-8 -*-


from django.conf.urls import url
from .views import Weixin

urlpatterns = [
    url(r'^$', Weixin.as_view(), name='weixin'),
]