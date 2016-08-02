from __future__ import unicode_literals

from django.db import models


class Fowler(models.Model):
    OpenID = models.CharField(max_length=100, unique=True)
    follow_time = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=100, default='None')

    def __unicode__(self):
        return self.OpenID



