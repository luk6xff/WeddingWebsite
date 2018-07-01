from django.test import TestCase
from guests.models import Event, Guest


class EventTest(TestCase):

    def setUp(self):
        self.event = Event.objects.create(
            name='Wesele'
        )
        self.guest1 = Guest.objects.create(
            event=self.event,
            first_name='Lukasz',
            last_name='Uszko',
        )
        self.guest2 = Guest.objects.create(
            event=self.event,
            first_name='Justyna',
            last_name='Pajak',
        )

    def tearDown(self):
        Event.objects.all().delete()

    def test_any_guests_attending_default(self):
        self.assertFalse(self.event.any_guests_attending)

    def test_any_guests_attending_false(self):
        self.guest1.is_attending = False
        self.guest1.save()
        self.guest2.is_attending = False
        self.guest2.save()
        self.assertFalse(self.event.any_guests_attending)

    def test_any_guests_attending_true(self):
        self.guest1.is_attending = False
        self.guest1.save()
        self.guest2.is_attending = True
        self.guest2.save()
        self.assertTrue(self.event.any_guests_attending)
