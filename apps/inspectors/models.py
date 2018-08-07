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
    ('Delaware', 'DE'),
    ('Maryland', 'MD'),
    ('Ohio', 'OH'),
    ('New York', 'NY'),
    )

    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    office = models.CharField(max_length=30, choices=OFFICE,
        default='None')
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
    is_employee = models.BooleanField(verbose_name="Is this your Employee?",
    default=False)


    def get_equipment_list(self):
        equipment = (Checkout.objects.filter(user=self, return_date__isnull=True))
        devices = []
        if equipment:
            for device in equipment:
                devices.append(device)
            return devices
    @property
    def get_current_project(self):
        projects = History.objects.filter(inspector=self).order_by("-stop_date")
        job = []
        if projects:
            for proj in projects:
                job.append(proj)
            if job[0].stop_date:
                return
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
        return f"{self.inspector.first_name} {self.inspector.last_name}: {self.body[:30]}"


class History(models.Model):
    inspector = models.ForeignKey('inspector', on_delete=models.CASCADE)
    job = models.ForeignKey('projects.Project', on_delete=models.CASCADE, null=True)
    start_date = models.DateField()
    stop_date = models.DateField(null=True, blank=True)

    def __str__(self):
        person = f"{self.inspector.first_name} {self.inspector.last_name}"
        job = self.job.name
        return f"{person}: {job}"
    
    @property 
    def duration(self):
        '''
        find duration on job by subtracting the stop date from the start date.
        If the job is still active use today as the theoretical stop date.
        '''
        if self.stop_date:
            stop_date = self.stop_date
        else:
            stop_date = datetime.now().date()
        days = (stop_date - self.start_date).days
        return float(days/ 365)