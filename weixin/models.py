# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Fowler(models.Model):
    OpenID = models.CharField(max_length=100, unique=True, verbose_name='用户ID')
    follow_time = models.DateTimeField(auto_now_add=True, verbose_name='关注时间')

    def __unicode__(self):
        return self.OpenID


class Dialog(models.Model):
    fowler = models.ForeignKey(Fowler)
    message = models.CharField(max_length=200, verbose_name='用户发送信息')
    reply = models.CharField(max_length=200, verbose_name='回复信息')
    time = models.DateTimeField(auto_now=True, verbose_name='时间')

    def __unicode__(self):
        return self.message


class Location(models.Model):
    fowler = models.ForeignKey(Fowler)
    x = models.FloatField(verbose_name='经度')
    y = models.FloatField(verbose_name='纬度')
    label = models.CharField(max_length=100, default='None', verbose_name='地理位置')
    time = models.DateTimeField(auto_now=True, verbose_name='时间')

    def __unicode__(self):
        return self.label


class Function(models.Model):
    keyword = models.CharField(max_length=100, unique=True, verbose_name='功能关键字')
    explain = models.CharField(max_length=200, verbose_name='功能解释')

    def __unicode__(self):
        return self.keyword
