import os
from datetime import datetime
from django.conf import settings
from django.urls import reverse
from django.http import Http404
from django.template.loader import render_to_string
from guests.models import Guest


def guess_guest_by_id_or_404(guest_id):
    try:
        return Guest.objects.get(pk=guest_id)
    except Guest.DoesNotExist:
        if settings.DEBUG:
            # in debug mode allow access by ID
            return Guest.objects.get(id=int(guest_id))
        else:
            raise Http404()


