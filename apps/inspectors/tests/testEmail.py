from django.core import mail
from django.test import TestCase

from inspectors.tests.helpers import rand_date, short_date
from inspectors.tasks import email_news_letter
from inspectors.models import Inspector, Notes
from projects.models import Project, Invoice
from profiles.models import Profile


class EmailTestCase(TestCase):
    maxDiff = None
    def setUp(self):
        I1 = Inspector.objects.create(
            first_name = "Markelle",
            last_name = "Tatum",
            office = "King of Prussia",
            classification = "TCI-2",
            address ="123 kitty lane",
            location = "Pittsburgh, PA",
            work_radius = 95,
            email = "marktest@prudenteng.com",
            phone_number = "3022993322",
            nicet_expiration = rand_date(),
            penndot_bituminous = rand_date(),
            necept_bituminous = rand_date(),
            penndot_concrete = rand_date(),
            aci_concrete = short_date()
        )
        I1.save()
        I2 = Inspector.objects.create(
            first_name = "Jim",
            last_name = "Irving",
            office = "King of Prussia",
            classification = "TCI-2",
            address ="123 kitty lane",
            location = "Pittsburgh, PA",
            work_radius = 95,
            email = "bardtest@prudenteng.com",
            phone_number = "3022993322",
            nicet_expiration = rand_date(),
            penndot_bituminous = rand_date(),
            necept_bituminous = rand_date(),
            penndot_concrete = rand_date(),
            aci_concrete = rand_date()
        )
        I2.save()
        self.N1 = Notes.objects.create(
            inspector = Inspector.objects.get(pk=I1.pk),
            body = "Isn't a real inspector, and won't trave to jobs"
        )
        self.N2 = Notes.objects.create(
            inspector = Inspector.objects.get(pk=I1.pk),
            body = "Has a 12 car garage"
        ).save()
        self.N3 = Notes.objects.create(
            inspector = Inspector.objects.get(pk=I2.pk),
            body = "Has a 12 car garage"
        ).save()
        p1 = Project.objects.create(
            prudent_number = '103.219',
            penndot_number = 'E01993',
            name = 'CP2',
            inspector = '',
            office = 'King of Prussia',
            start_date = short_date(),
            end_date = short_date(),
            straight_hours_budget = 300.0,
            overtime_hours_budget = 25.0,
            payroll_budget = 60000.00,
            other_cost_budget = 10000.00,
        )
        p2 = Project.objects.create(
            prudent_number = '103.111',
            penndot_number = 'E01994',
            name = 'Septa bridge over mars',
            inspector = '',
            office = 'King of Prussia',
            start_date = short_date(),
            end_date = short_date(),
            straight_hours_budget = 300.0,
            overtime_hours_budget = 25.0,
            payroll_budget = 18200.00,
            other_cost_budget = 4500.00,
        )
        i1 = Invoice.objects.create(
            project = p1,
            estimate_number = 1,
            start_date = short_date(),
            end_date = short_date(),
            labor_cost= 16000,
            other_cost = 600,
            straight_hours = 13,
            overtime_hours = 16,
            invoice_number = '19961',
        )
        i2 = Invoice.objects.create(
            project = p1,
            estimate_number = 2,
            start_date = short_date(),
            end_date = short_date(),
            labor_cost = 25000,
            other_cost = 1250,
            straight_hours = 13,
            overtime_hours = 16,
            invoice_number = '19962',
        ).save()
        i3 = Invoice.objects.create(
            project = p1,
            estimate_number = 3,
            start_date = short_date(),
            end_date = short_date(),
            labor_cost = 11260.90,
            other_cost = 505.11,
            straight_hours = 13.00,
            overtime_hours = 16.00,
            invoice_number = '021993',
        ).save()

    # def test_inspector_certs(self):
    #     self.assertEqual(check_inspector_certs("King of Prussia"), 'zzz')


    def test_email_message(self):
        subject, message = email_news_letter()
        mail.send_mail(
        subject,
        message,
        'noreply@officeassistant.com',
        ['rlawson@prudenteng.com']
        ),
        html_message=message
        #self.assertEqual(self.p1.prudent_number, '103.217')
        self.assertEqual(mail.outbox[0].body, 'EMAIL LUL')
