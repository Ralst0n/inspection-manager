from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
# Create your models here.
class Invoice(models.Model):
    """
    Represents an Invoice from creation to final
    """
    STATUS_CODE = (
        (0, 'DRAFT'),
        (1, 'AWAITING MANAGER APPROVAL'),
        (2, 'AWAITING REVIEWER APPROVAL'),
        (3, 'APPROVED FOR SUBMISSION'),
    )
    project = models.ForeignKey('projects.project', on_delete=models.CASCADE)
    estimate_number = models.DecimalField(
        max_digits=3, decimal_places=0)
    start_date = models.DateField()
    end_date = models.DateField()
    labor_cost = models.DecimalField(max_digits=9, decimal_places=2,
     blank=True, null=True)
    other_cost = models.DecimalField(max_digits=9, decimal_places=2,
     blank=True, null=True)
    straight_hours = models.DecimalField(max_digits=9, decimal_places=2,
     blank=True, null=True)
    overtime_hours = models.DecimalField(max_digits=9, decimal_places=2,
     blank=True, null=True)
    invoice_number = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True,
        help_text="Prudent invoice number i.e. 17176"
    )
    invoice_file = models.FileField('invoices/')

    # Automatically created fields
    created_at= models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CODE, default=0)
    last_modified = models.DateField(auto_now=True, null=True)
    last_modified_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='modifier')

    def __str__(self):
        return f"{self.project.prudent_number} #{self.estimate_number}"

    @property
    def name(self):
        return f"{self.project.prudent_number} #{self.estimate_number}"

    @property
    def office(self):
        return self.project.office

    @property
    def readable_status(self):
        return self.STATUS_CODE[self.status][1].capitalize()

    def get_absolute_url(self):
        """
        Returns the url to access a particular invoice.
        """
        return reverse('invoices:details', args=[self.id])
    @property
    def total_cost(self):
        return self.labor_cost + self.other_cost

class Comments(models.Model):
    invoice = models.ForeignKey('invoice', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.creator} {self.body[0:30]}"
