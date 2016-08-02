from __future__ import unicode_literals
import time

from django.db import models
from django.utils import timezone


class Fowler(models.Model):
    OpenID = models.CharField(max_length=100, unique=True)
    follow_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.OpenID



