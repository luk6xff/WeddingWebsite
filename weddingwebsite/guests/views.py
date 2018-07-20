import base64
from collections import namedtuple
import random
from datetime import datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Count, Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
from guests import csv_import
from guests.models import Guest
from .forms import RsvpForm



class GuestListView(ListView):
    model = Guest


@login_required
def export_guests(request):
    export = csv_import.export_guests()
    response = HttpResponse(export.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=all-guests.csv'
    return response


@login_required
def dashboard(request):
    return render(request, 'guests/dashboard.html', context={
        'guests': Guest.objects.filter(is_attending=True).count(),
        'possible_guests': Guest.objects.filter(is_invited=True).exclude(is_attending=False).count(),
        'not_coming_guests': Guest.objects.filter(is_attending=False).count(),
        'pending_guests': Guest.objects.filter(is_invited=True, is_attending=None).count(),
        'total_invites': Guest.objects.filter(is_invited=True).count()
    })


def rsvp(request):
    if request.method == 'POST':
        form = RsvpForm(request.POST)
        if form.is_valid():
            print("sending email")
    else:
        form = RsvpForm()
    return render(request, 'guests/rsvp.html', {'form': form})



