import base64
from collections import namedtuple
import random
from datetime import datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import ListView
from guests import csv_import
from guests.models import Guest
from .forms import RsvpForm, RsvpGuestsNumForm
from django.core.mail import send_mail
from django.http import Http404  



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


def rsvp(request, guests_num):
    sent = False
    if request.method == 'POST':
        form = RsvpForm(guests_num, request.POST)
        if form.is_valid():
            prepare_and_send_rsvp_email(form)
            sent = True
    else:
        if guests_num > 10 or guests_num < 1:
            raise Http404
        form = RsvpForm(guests_num)
    return render(request, 'guests/rsvp.html', {'form': form, 'guests_num': guests_num, 'sent': sent})


def rsvp_guests_num(request):
    if request.method == 'POST':
        form = RsvpGuestsNumForm(request.POST)
        if form.is_valid():
            return redirect('rsvp', guests_num=form['guests_num'].value())
    else:
        form = RsvpGuestsNumForm()
    return render(request, 'guests/rsvp_guests_num.html', {'form': form})


def prepare_and_send_rsvp_email(form):
    cd = form.cleaned_data
    subject = "New wedding presence confirmation from {}".format(cd['name 0'])
    msg = "Hello Justynka & Łukasz, just got new wedding confirmation from {}\n\n\n".format(cd['name 0'])
    msg += "SENDER_GUEST_NAME: {}\n".format(cd['name 0'])
    msg += "PRESENCE_STATUS: {}\n".format(cd["presence_confirmation 0"])
    msg += "HOTEL: {}\n\n".format(cd["hotel_needed 0"])
    for key, val in cd.items():
        if key.startswith('name') and key != 'name 0':
            msg += "GUEST_NAME: {}\n".format(val)
            num = key.split(' ')[1]
            msg += "PRESENCE_STATUS: {}\n".format(cd["presence_confirmation {}".format(num)])
            msg += "HOTEL: {}\n\n".format(cd["hotel_needed {}".format(num)])
    msg += "EMAIL: {}\n".format(cd["email"])
    msg += "COMMENTS: {}\n\n\n".format(cd["comments"])
    print(cd)
    print("sending email...")
    send_mail(subject, msg, "lukasz.uszko@gmail.com", ("lukasz.uszko@gmail.com", "justyna12pajak@gmail.com"))