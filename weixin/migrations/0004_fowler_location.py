# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-02 18:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weixin', '0003_auto_20160802_1707'),
    ]

    operations = [
        migrations.AddField(
            model_name='fowler',
            name='location',
            field=models.CharField(default='None', max_length=100),
        ),
    ]