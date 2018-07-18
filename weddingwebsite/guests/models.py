from __future__ import unicode_literals
import datetime
import uuid

from django.db import models
from django.dispatch import receiver


def _random_uuid():
    return uuid.uuid4().hex


class Event(models.Model):
    """
    A event consists of one or more guests.
    """
    name = models.TextField()
    invitation_closed = models.DateTimeField(null=True, blank=True, default=None)
    comments = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return 'Event: {}'.format(self.name)

    @classmethod
    def in_default_order(cls):
        return cls.objects.order_by('name')

    @property
    def ordered_guests(self):
        return self.guest_set.order_by('is_child', 'pk')

    @property
    def any_guests_attending(self):
        return any(self.guest_set.values_list('is_attending', flat=True))

    @property
    def guest_emails(self):
        return filter(None, self.guest_set.values_list('email', flat=True))

LANGUAGE = [
    ('PL', 'polski'),
    ('ENG','english')
]


class Guest(models.Model):
    """
    A single guest
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    first_name = models.TextField()
    last_name = models.TextField(null=True, blank=True)
    email = models.TextField(null=True, blank=True)
    phone_number = models.TextField(null=True, blank=True)
    is_invited = models.BooleanField(default=False)
    is_attending = models.NullBooleanField(default=None)
    is_child = models.BooleanField(default=False)
    use_hotel = models.BooleanField(default=False)
    language = models.CharField(max_length=10, choices=LANGUAGE, default=LANGUAGE[0])
    comments = models.TextField(null=True, blank=True)

    @property
    def name(self):
        return u'{} {}'.format(self.first_name, self.last_name)

    @property
    def unique_id(self):
        # convert to string so it can be used in the "add" template tag
        return unicode(self.pk)

    def __unicode__(self):
        return 'Guest: {} {}'.format(self.first_name, self.last_name)
