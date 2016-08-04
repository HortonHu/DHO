from django.contrib import admin

from .models import Fowler, Dialog, Location, Function


class FowlerAdmin(admin.ModelAdmin):
    list_display = ('OpenID', 'follow_time')
    search_fields = ('OpenID', 'follow_time')
    list_filter = ('follow_time',)
    date_hierarchy = 'follow_time'

    # fields = ('follow_time', )


class DialogAdmin(admin.ModelAdmin):
    list_display = ('fowler', 'message', 'reply', 'time')
    list_filter = ('time', 'fowler', )
    search_fields = ('message', 'reply')


class LocationAdmin(admin.ModelAdmin):
    list_display = ('fowler', 'label', 'x', 'y', 'time')
    list_filter = ('time', 'label', )
    search_fields = ('label', )


class FunctionAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'explain')


admin.site.register(Fowler, FowlerAdmin)
admin.site.register(Dialog, DialogAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Function, FunctionAdmin)

