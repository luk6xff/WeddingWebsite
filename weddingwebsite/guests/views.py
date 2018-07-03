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
from guests.rsvp import guess_guest_by_id_or_404
from guests.models import Guest


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


def rsvp(request, guest_id):
    guest = guess_guest_by_id_or_404(guest_id)
    if guest.invitation_opened is None:
        guest.invitation_opened = datetime.utcnow()
        guest.save()
    if request.method == 'POST':
        print(request.POST) #TODO
        if request.POST.get('comments'):
            comments = request.POST.get('comments')
            guest.comments = comments if not guest.comments else '{}; {}'.format(guest.comments, comments)
        guest.is_attending = guest.any_guests_attending
        guest.save()
        return HttpResponseRedirect(reverse('rsvp-confirm', args=[guest_id]))
    return render(request, template_name='guests/rsvp.html', context={
        'guest': guest,
    })


def rsvp_confirm(request, guest_id=None):
    guest = guess_guest_by_id_or_404(guest_id)
    return render(request, template_name='guests/rsvp_confirmation.html', context={
        'guest': guest,
        'support_email': settings.DEFAULT_WEDDING_REPLY_EMAIL,
    })


def _base64_encode(filepath):
    with open(filepath, "rb") as image_file:
        return base64.b64encode(image_file.read())
