from django.contrib import admin
from .models import Guest, Event


class GuestInline(admin.TabularInline):
    model = Guest
    fields = ('first_name', 'last_name', 'email', 'is_attending', 'is_child')
    readonly_fields = ('first_name', 'last_name', 'email')


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'invitation_closed')
    list_filter = ('name', 'invitation_closed')
    inlines = [GuestInline]


class GuestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'event', 'email', 'is_attending', 'is_child')
    list_filter = ('is_attending', 'is_child', 'event__name')


admin.site.register(Event, EventAdmin)
admin.site.register(Guest, GuestAdmin)
