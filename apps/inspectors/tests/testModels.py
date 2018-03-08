from django.test import TestCase

from inspectors.models import Inspector, Notes
from inspectors.newsletters import check_invoice_created
class InspectorModelTest(TestCase):
    def setUp(self):
        self.I1 = Inspector.objects.create(
            first_name = "Mark",
            last_name = "Test",
            office = "King of Prussia",
            classification = "TCI-2",
            address ="123 kitty lane",
            location = "Pittsburgh, PA",
            work_radius = 95,
            email = "marktest@prudenteng.com",
            phone_number = "3022993322",
        )
        self.I2 = Inspector.objects.create(
            first_name = "bard",
            last_name = "Test",
            office = "King of Prussia",
            classification = "TCI-2",
            address ="123 kitty lane",
            location = "Pittsburgh, PA",
            work_radius = 95,
            email = "bardtest@prudenteng.com",
            phone_number = "3022993322",
        )
        self.N1 = Notes.objects.create(
            inspector = self.I1,
            body = "Isn't a real inspector, and won't trave to jobs"
        )
        self.N2 = Notes.objects.create(
            inspector = self.I1,
            body = "Has a 12 car garage"
        )
        self.N3 = Notes.objects.create(
            inspector = self.I2,
            body = "Has a 12 car garage"
        )

    def test_create_inspector(self):
        self.assertEqual(Inspector.objects.count(), 2)

    def test_inspector_notes(self):
        '''
         notes properly created and correct number attributed
         based on inspector
        '''
        self.assertEqual(Notes.objects.count(), 3)
        self.assertEqual(self.I1.notes_set.count(), 2)

    def test_inspector_something(self):
        '''really we just adding a 3rd test just to be doing it to try out vim'''
        self.assertEqual(self.I1.work_radius, 95)


#https://scotch.io/tutorials/build-a-rest-api-with-django-a-test-driven-approach-part-1
