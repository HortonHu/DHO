from django.contrib import admin

from .models import Fowler


class FowlerAdmin(admin.ModelAdmin):
    list_display = ('OpenID', 'follow_time', 'location')


admin.site.register(Fowler, FowlerAdmin)

