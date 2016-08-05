# -*- coding:utf-8 -*-


from django.conf.urls import url
from .views import Weixin, Token

urlpatterns = [
    url(r'^$', Weixin.as_view(), name='weixin'),
    url(r'^$', Token.as_view(), name='token'),
]