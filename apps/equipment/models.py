from django.db import models
from django.urls import reverse
# Create your models here.
class Equipment(models.Model):
    DEVICE_TYPE = (
    ('iPhone', 'iPhone'),
    ('iPad', 'iPad'),
    ('Laptop', 'Laptop'),
    )

    OFFICE = (
    ('King of Prussia', 'KOP'),
    ('Pittsburgh', 'PGH'),
    ('Test', 'TEST'),
    ('None', 'None')
    )

    name = models.CharField(max_length=60, help_text="i.e. kopfield1")
    office = models.CharField(max_length=30,
        choices=OFFICE, default="King of Prussia")
    device = models.CharField(max_length= 35, choices=DEVICE_TYPE)
    serial_number = models.CharField(max_length=40)
    phone_number = models.CharField(max_length=18, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('equipment-detail', args=[str(self.id)])

    def get_current_user(self):
        """
        get the most recent user of the object
        """
        #to get just the user append the field name to end of search
        if Checkout.objects.filter(item=self).order_by(
                '-checkout_date').exists():
            first_name = Checkout.objects.filter(
                item=self).order_by('-checkout_date').first().user.first_name
            last_name = Checkout.objects.filter(
                item=self).order_by('-checkout_date').first().user.last_name
            return "{} {}".format(first_name, last_name)
    
    @property
    def current_user(self):
        """
        get the most recent user of the object
        """
        if self.checkout_set.filter(return_date__isnull=True).count() == 0:
            return None
        return self.checkout_set.get(return_date__isnull=True).user

class Checkout(models.Model):
    item = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    user = models.ForeignKey('inspectors.Inspector', on_delete=models.CASCADE, null=True)
    checkout_date = models.DateField()
    return_date = models.DateField(blank=True, null=True,
    help_text="leave blank if item is still out")

    class Meta:
        ordering = ["-checkout_date"]

    def __str__(self):
        return "{} - {} {} - {}".format( self.item.name,  self.user.first_name,
        self.user.last_name,self.item.device)
