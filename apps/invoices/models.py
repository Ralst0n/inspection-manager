from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse
from django.utils import timezone

# Create your models here.
class Invoice(models.Model):
    STATUS_CODE = (
        (0, 'DRAFT'),
        (1, 'AWAITING MANAGER APPROVAL'),
        (2, 'AWAITING REVIEWER APPROVAL'),
        (3, 'APPROVED FOR SUBMISSION'),
    )
    name = models.CharField(max_length=25)
    invoice_file = models.FileField('invoices')
    created_at= models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CODE, default=0)
    last_modified = models.DateField(auto_now=True, null=True)
    last_modified_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='modifier')

    def __str__(self):
        return self.name

    @property
    def readable_status(self):
        return self.STATUS_CODE[self.status][1].lower()

    def get_absolute_url(self):
        """
        Returns the url to access a particular invoice.
        """
        return reverse('invoices:details', args=[self.id])

class Comments(models.Model):
    invoice = models.ForeignKey('invoice', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.creator} {self.body[0:30]}"
