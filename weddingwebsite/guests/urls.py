
from django.urls import path, include
from guests.views import GuestListView, export_guests, rsvp, dashboard

urlpatterns = [
    path(r'guests', GuestListView.as_view(), name='guest-list'),
    path(r'dashboard', dashboard, name='dashboard'),
    path(r'guests/export', export_guests, name='export-guest-list'),
    path(r'rsvp', rsvp, name='rsvp'),
]
