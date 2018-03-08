from datetime import date, datetime, timedelta

from django.test import TestCase

from projects.models import Project, Invoice
from inspectors.models import Inspector


class ProjectModelTest(TestCase):
    def setUp(self):
        date_1 = date.today()
        date_2 = date_1 + timedelta(days=10)
        p1 = Project.objects.create(
            prudent_number = '103.219',
            penndot_number = 'E01993',
            name = 'CP2',
            inspector = [Inspector.objects.create(
                    id=2,
                    first_name = "bard",
                    last_name = "Test",
                    office = "King of Prussia",
                    classification = "TCI-2",
                    address ="123 kitty lane",
                    location = "Pittsburgh, PA",
                    work_radius = 95,
                    email = "bardtest@prudenteng.com",
                    phone_number = "3022993322"
                ).save()],
            office = 'King of Prussia',
            start_date = date_1,
            end_date = date_2,
            st_hours = 300,
            ot_hours = 25,
            payroll_budget = 132000,
            other_cost_budget = 10000,
        )
        p2 = Project.objects.create(
            prudent_number = '103.111',
            penndot_number = 'E01994',
            name = 'Septa bridge over mars',
            inspector = [Inspector.objects.create(
                id=1,
                first_name = "Mark",
                last_name = "Test",
                office = "King of Prussia",
                classification = "TCI-2",
                address ="123 kitty lane",
                location = "Pittsburgh, PA",
                work_radius = 95,
                email = "marktest@prudenteng.com",
                phone_number = "3022993322",
            ).save()],
            office = 'King of Prussia',
            start_date = date_1,
            end_date = date_2,
            st_hours = 300,
            ot_hours = 25,
            payroll_budget = 132000,
            other_cost_budget = 10000,
        )
        i1 = Invoice.objects.create(
            project = p1,
            estimate_num = 1,
            start_date = date_1,
            end_date = date_1 + timedelta(days=3),
            payroll= 11260.90,
            other_cost = 505.11,
            st_hours = 13,
            ot_hours = 16,
            invoice_num = '19961',
        )
        i2 = Invoice.objects.create(
            project = p1,
            estimate_num = 2,
            start_date = date_1,
            end_date = date_1 + timedelta(days=-3),
            payroll = 32134.90,
            other_cost = 505.11,
            st_hours = 13,
            ot_hours = 16,
            invoice_num = '19962',
        )
        i3 = Invoice.objects.create(
            project = p2,
            estimate_num = 2,
            start_date = date_1,
            end_date = date_1 + timedelta(days=-3),
            payroll = 11260.90,
            other_cost = 505.11,
            st_hours = 13,
            ot_hours = 16,
            invoice_num = '19963',
        )

    def test_project_creation(self):
        ''' Project manager accounts for all 3 invoices created'''
        project_count = Project.objects.count()
        self.assertEqual(project_count, 2)

    def test_invoice_creation(self):
        ''' Invoice manager accounts for all 3 invoices created'''
        invoice_count = Invoice.objects.count()
        self.assertEqual(invoice_count, 3)

    def test_budget_totals(self):
        '''sum of payroll for associated invoices'''
        p1 = Project.objects.last()
        self.assertEqual(p1.payroll_to_date, (11260.90 + 32134.90))
        self.assertEqual(p1.other_cost_to_date, 1010.22)
    # def test_total_other_cost(self):
    #     '''sum of other cost in all associated invoices'''
    #     p1 = Project.objects.last()
    #     self.assertEqual(p1)
    def test_last_invoiced(self):
        ''' Returns end date of most recent invoice  in mm/dd/yyyy format'''
        p1 = Project.objects.last()
        self.assertEqual(p1.last_invoiced, datetime.strftime(date.today() + timedelta(days=3),"%m/%d/%Y"))

    def test_burn_rate_calc(self):
        '''Calculates months remaining at current rate'''
        p1 = Project.objects.last()
        self.assertEqual(p1.is_almost_finished(), 4)
        # Make sure its recalculated after a new invoice
        Invoice.objects.create(
            project = p1,
            estimate_num = 3,
            start_date = date.today(),
            end_date = date.today() + timedelta(days=-15),
            payroll = 25000.90,
            other_cost = 505.11,
            st_hours = 13,
            ot_hours = 16,
            invoice_num = '19964',
        )
        self.assertEqual(p1.is_almost_finished(), 3)
