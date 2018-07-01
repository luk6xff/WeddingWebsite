import csv
from io import StringIO
import uuid
from guests.models import Event, Guest


def import_guests(path):
    with open(path, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        first_row = True
        for row in reader:
            if first_row:
                first_row = False
                continue
            event_name, first_name, last_name, event_type, is_child, category, is_invited, email = row[:8]
            if not event_name:
                print('skipping row {}'.format(row))
                continue
            event = Event.objects.get_or_create(name=event_name)[0]
            event.type = event_type
            event.category = category
            event.is_invited = _is_true(is_invited)
            if not event.invitation_id:
                event.invitation_id = uuid.uuid4().hex
            event.save()
            if email:
                guest, created = Guest.objects.get_or_create(event=event, email=email)
                guest.first_name = first_name
                guest.last_name = last_name
            else:
                guest = Guest.objects.get_or_create(event=event, first_name=first_name, last_name=last_name)[0]
            guest.is_child = _is_true(is_child)
            guest.save()


def export_guests():
    headers = [
        'first_name', 'last_name', 'event_name', 
        'is_child', 'is_invited', 'is_attending', 'email', 'comments'
    ]
    file = StringIO()
    writer = csv.writer(file)
    writer.writerow(headers)
    for event in Event.in_default_order():
        for guest in event.guest_set.all():
            if guest.is_attending:
                writer.writerow([ 
                    guest.first_name,
                    guest.last_name,
                    event.name,
                    guest.is_child,
                    guest.is_invited,
                    guest.is_attending,
                    guest.email,
                    guest.phone_number,
                    event.comments,
                ])
    return file


def _is_true(value):
    value = value or ''
    return value.lower() in ('y', 'yes')
