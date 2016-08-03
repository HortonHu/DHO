from django.contrib import admin

from .models import Fowler, Dialog, Location, Function


class FowlerAdmin(admin.ModelAdmin):
    list_display = ('OpenID', 'follow_time')
    search_fields = ('OpenID', 'follow_time')
    list_filter = ('follow_time',)
    date_hierarchy = 'follow_time'

    fields = ('location', )


admin.site.register(Fowler, FowlerAdmin)
admin.site.register(Dialog)
admin.site.register(Location)
admin.site.register(Function)

