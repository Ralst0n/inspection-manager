from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from datetime import datetime, timedelta

from apps.equipment.models import Checkout
from apps.projects.models import Project

# Create your models here.
class Inspector(models.Model):
    """
    model representing a CI
    """

    CI_TYPE = (
    ('TA-1', 'TA-1'),
    ('TA-2', 'TA-2'),
    ('TCI-1', 'TCI-1'),
    ('TCI-2', 'TCI-2'),
    ('TCI-3', 'TCI-3'),
    ('TCIS-1', 'TCIS-1'),
    ('TCIS-2', 'TCIS-2'),
    ('TCM', 'TCM'),
    )

    OFFICE = (
    ('King of Prussia', 'KOP'),
    ('Pittsburgh', 'PGH'),
    ('Test', 'TEST'),
    ('None', 'None')
    )

    STATE = (
    ('Pennsylvania', 'PA'),
    ('New Jersey', 'NJ'),
    ('Maryland', 'MD'),
    ('Ohio', 'OH'),
    ('New York', 'NY'),
    )

    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    office = models.CharField(max_length=30, choices=OFFICE,
        default='King of Prussia')
    classification = models.CharField(max_length=6, choices=CI_TYPE, blank=True,
        default='TA-1', help_text='inspector classification i.e. TCI-2')
    address = models.CharField(max_length=100, help_text="i.e. '321 Atwood St'",
        null=True)
    home_city = models.CharField(max_length=100, blank=True)
    home_state = models.CharField(max_length=100, choices=STATE, blank=True)
    home_zip = models.CharField(max_length=5, blank=True)
    work_radius = models.DecimalField(max_digits=3, help_text='number of miles',
        decimal_places=0)
    email = models.EmailField(verbose_name="E-mail", max_length=60)
    phone_number = models.CharField(max_length=10, blank=True)
    is_employee = models.BooleanField(verbose_name="Your Employee?",
        default=False)
    nicet_expiration = models.DateField("NICET Expiration", blank=True,
        null=True)
    penndot_bituminous = models.DateField("PennDOT Bituminous Expiration",
        blank=True, null=True)
    necept_bituminous = models.DateField("NECEPT Expiration", blank=True,
        null=True)
    penndot_concrete = models.DateField("PennDOT Concrete Expiration",
        blank=True, null=True)
    aci_concrete = models.DateField("ACI Concrete Expiration", blank=True,
        null=True)
    district_1_experience = models.DecimalField(max_digits=3, decimal_places=1,
        help_text="this is a number of years", null=True, default=0
    )
    district_2_experience = models.DecimalField(max_digits=3, decimal_places=1,
        help_text="this is a number of years", null=True, default=0)
    district_3_experience = models.DecimalField(max_digits=3, decimal_places=1,
        help_text="this is a number of years", null=True, default=0)
    district_4_experience = models.DecimalField(max_digits=3, decimal_places=1,
        help_text="this is a number of years", null=True, default=0)
    district_5_experience = models.DecimalField(max_digits=3, decimal_places=1,
        help_text="this is a number of years", null=True, default=0)
    district_6_experience = models.DecimalField(max_digits=3, decimal_places=1,
        help_text="this is a number of years", null=True, default=0)
    district_8_experience = models.DecimalField(max_digits=3, decimal_places=1,
        help_text="this is a number of years", null=True, default=0)
    district_9_experience = models.DecimalField(max_digits=3, decimal_places=1,
        help_text="this is a number of years", null=True, default=0)
    district_10_experience = models.DecimalField(max_digits=3, decimal_places=1,
        help_text="this is a number of years", null=True, default=0)
    district_11_experience = models.DecimalField(max_digits=3, decimal_places=1,
        help_text="this is a number of years", null=True, default=0)
    district_12_experience = models.DecimalField(max_digits=3, decimal_places=1,
        help_text="this is a number of years", null=True, default=0)

    def get_equipment_list(self):
        equipment = (Checkout.objects.filter(user=self, return_date__isnull=True))
        devices = []
        if equipment:
            for device in equipment:
                devices.append(device)
            return devices

    def get_current_project(self):
        project = History.objects.filter( inspector=self)
        job = []
        if project:
            for proj in project:
                job.append(proj)
            return job

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        """
        Returns the url to access a particular inspector.
        """
        return reverse('inspector-detail', args=[str(self.id)])

class Notes(models.Model):
    inspector = models.ForeignKey('inspector', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{datetime.strftime(self.created_at, '%m/%d/%Y')} {self.inspector.first_name} {self.inspector.last_name}"


class History(models.Model):
    inspector = models.ForeignKey('inspector', on_delete=models.CASCADE)
    job = models.ForeignKey('projects.Project', on_delete=models.CASCADE, null=True)
    start_date = models.DateField()
    stop_date = models.DateField(null=True)

    def __str__(self):
        person = f"{self.inspector.first_name} {self.inspector.last_name}"
        job = self.job.name
        return f"{person}: {job}"
    
    @property 
    def duration(self):
        return self.stop_date - self.start_date
    