from __future__ import unicode_literals

from django.db import models


class Fowler(models.Model):
    OpenID = models.CharField(max_length=100)


