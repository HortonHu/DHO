# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-03 08:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weixin', '0008_auto_20160803_1601'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dialog',
            options={'verbose_name_plural': '\u5bf9\u8bdd\u4fe1\u606f'},
        ),
        migrations.AlterModelOptions(
            name='fowler',
            options={'verbose_name_plural': '\u5173\u6ce8\u8005'},
        ),
        migrations.AlterModelOptions(
            name='function',
            options={'verbose_name_plural': '\u529f\u80fd'},
        ),
        migrations.AlterModelOptions(
            name='location',
            options={'verbose_name_plural': '\u5730\u7406\u4f4d\u7f6e\u4fe1\u606f'},
        ),
    ]