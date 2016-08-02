# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Fowler(models.Model):
    OpenID = models.CharField(max_length=100, unique=True, verbose_name='用户ID')
    follow_time = models.DateTimeField(auto_now_add=True, verbose_name='关注时间')
    location = models.CharField(max_length=100, default='None', verbose_name='地理位置')

    def __unicode__(self):
        return self.OpenID



