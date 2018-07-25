
from django.urls import path, include
from guests.views import GuestListView, export_guests, rsvp, rsvp_guests_num, dashboard

urlpatterns = [
    path(r'guests', GuestListView.as_view(), name='guest-list'),
    path(r'dashboard', dashboard, name='dashboard'),
    path(r'guests/export', export_guests, name='export-guest-list'),
    path(r'rsvp/<int:guests_num>/', rsvp, name='rsvp'),
    path(r'rsvp_start', rsvp_guests_num, name='rsvp_guests_num'),
]
