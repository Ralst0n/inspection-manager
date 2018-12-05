from django.test import TestCase

from apps.inspectors.models import Inspector
from .models import Equipment, Checkout
# Create your tests here.


class ModelsTestCase(TestCase):
    def setUp(self):

        # Create Equipments
        e1 = Equipment.objects.create(
            name="tester1",
            device="iPad",
            serial_number="1"
        )
        e2 = Equipment.objects.create(
            name="tester2",
            device="iPhone",
            serial_number="2"
        )
        i1 = Inspector.objects.create(
            first_name="jo",
            last_name="blo",
            work_radius="33",
            email="guy@3.com"
        )

        # Create Checkouts
        Checkout.objects.create(
            item=e1,
            user=i1,
            checkout_date="3/3/19"
        )

    def test_equipment_count(self):
        assertEquals(Equipment.objects.count(), 2)
