import os
from django.test import TestCase
from guests.csv_import import import_guests
from guests.models import Event, Guest


class GuestImporterTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super(GuestImporterTest, cls).setUpClass()
        cls.path = os.path.join(os.path.dirname(__file__), 'data', 'guests-test.csv')
        import_guests(cls.path)

    def test_import(self):
        self.assertEqual(3, Event.objects.count())
        self.assertEqual(5, Guest.objects.count())
        the_starks = Guest.objects.filter(event__name='The Starks')
        self.assertEqual(3, the_starks.count())

    def test_import_idempotent(self):
        for i in range(3):
            import_guests(self.path)
            self.assertEqual(3, Event.objects.count())
            self.assertEqual(5, Guest.objects.count())
            the_starks = Guest.objects.filter(event__name='The Starks')
            self.assertEqual(3, the_starks.count())

    def test_is_child(self):
        for guest in Guest.objects.all():
            if guest.first_name == 'Arya':
                self.assertTrue(guest.is_child)
            else:
                self.assertFalse(guest.is_child)

    def test_is_invited(self):
        for event in Event.objects.all():
            if event.name == 'Jaime':
                self.assertFalse(event.is_invited)
            else:
                self.assertTrue(event.is_invited)

    def test_event_type(self):
        for guest in Guest.objects.all():
            if guest.last_name == 'Stark':
                self.assertEqual('formal', guest.event.type)
            else:
                self.assertEqual('fun', guest.event.type)

    def test_email(self):
        self.assertEqual('ned@winterfell.gov', Guest.objects.get(first_name='Lukasz').email)

    def test_email_default(self):
        self.assertEqual(None, Guest.objects.get(first_name='Tyrion').email)

    def test_category(self):
        self.assertEqual('starks', Event.objects.get(name='The Starks').category)
        self.assertEqual('lannisters', Event.objects.get(name='Jaime').category)
