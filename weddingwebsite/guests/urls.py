from django.conf.urls import url

from guests.views import GuestListView, export_guests, rsvp, rsvp_confirm, dashboard

urlpatterns = [
    url(r'^guests/$', GuestListView.as_view(), name='guest-list'),
    url(r'^dashboard/$', dashboard, name='dashboard'),
    url(r'^guests/export$', export_guests, name='export-guest-list'),
    url(r'^rsvp/(?P<guest_id>[\w-]+)/$', rsvp, name='rsvp'),
    url(r'^rsvp/confirm/(?P<guest_id>[\w-]+)/$', rsvp_confirm, name='rsvp-confirm'),
]
