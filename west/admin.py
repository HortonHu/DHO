from django.contrib import admin
from west.models import Character, Contact, Tag


class TagInLine(admin.TabularInline):
    model = Tag


class ContactAdmin(admin.ModelAdmin):
    inlines = [TagInLine]
    fieldsets = (
        ['Main', {
            'fields': ('name', 'email'),
        }],
        ['Advance', {
            'classes': ('collapse', ),
            'fields': ('age', ),
        }]
    )
    list_display = ('name', 'age', 'email')
    search_fields = ('name', )

admin.site.register(Contact, ContactAdmin)
admin.site.register([Character, Tag])
