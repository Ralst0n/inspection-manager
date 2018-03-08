from django.test import TestCase

from datetime import date, datetime, timedelta

from inspectors.models import Inspector
from partners.models import BusinessPartner
from projects.models import Project, Invoice

date_1 = date.today()
date_2 = date_1 + timedelta(days=10)

class ProjectModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        STAR = Inspector.objects.create(
                id=2,
                first_name = "bard",
                last_name = "Test",
                office = "King of Prussia",
                classification = "TCI-2",
                address ="123 kitty lane",
                work_radius = 95,
                email = "bardtest@prudenteng.com",
                phone_number = "3022993322"
            )
        b = Inspector.objects.get(id=2)

        Project.objects.create(
            prudent_number = '103.219',
            penndot_number = 'E01993',
            name = 'CP2',
            business_partner = BusinessPartner.objects.create(
                name="Pennoni Associates Incorporated"
            ),
            inspector = b,
            office = 'King of Prussia',
            start_date = date_1,
            end_date = date_2,
            st_hours = 300,
            ot_hours = 25,
            payroll_budget = 132000,
            other_cost_budget = 10000,
        )

    def test_project_creation(self):
        self.assertEqual(Project.objects.count(), 1)
