from django.contrib import admin

from .models import Fowler


class FowlerAdmin(admin.ModelAdmin):
    list_display = ('OpenID', 'follow_time', 'location')
    search_fields = ('OpenID', 'follow_time', 'location')
    list_filter = ('follow_time', 'location')
    date_hierarchy = 'follow_time'

    fields = ('location', )


admin.site.register(Fowler, FowlerAdmin)

