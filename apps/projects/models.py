from django.db import models
from django.db.models import Sum
from django.urls import reverse
from datetime import datetime, date


# Create your models here.
class Project(models.Model):
    """
    Model representing a project
    """
    OFFICE = (
    ('King of Prussia', 'KOP'),
    ('Pittsburgh', 'PGH'),
    ('Test', 'TEST')
    )

    prudent_number = models.CharField(max_length=7, help_text="i.e. 101.083", primary_key=True)
    penndot_number = models.CharField(max_length=6, help_text="i.e. E02430")
    office = models.CharField(max_length=30, choices=OFFICE, default='King of Prussia')
    name = models.CharField(max_length=100)
    district = models.DecimalField(max_digits=2, decimal_places=0)
    business_partner = models.ForeignKey('partners.BusinessPartner',
        on_delete=models.CASCADE, null=True)
    start_date = models.DateField()
    payroll_budget = models.DecimalField(max_digits=9, decimal_places=2, default=30000.00)
    other_cost_budget = models.DecimalField(max_digits=9, decimal_places=2, default=30000.00)
    straight_hours_budget = models.DecimalField(max_digits=9, decimal_places=2, default=2000.0)
    overtime_hours_budget = models.DecimalField(max_digits=9, decimal_places=2, default=2000.0)
    active = models.BooleanField(default=True, help_text="Is this project actively being worked on?")
    completed = models.BooleanField(default=False)
    budget_letter = models.BooleanField(verbose_name="75 percent letter sent", default=False)

    def __str__(self):
        return f"{self.penndot_number}: {self.name}"

    def get_absolute_url(self):
        return reverse('project-detail', args=[str(self.prudent_number)])

    @property
    def payroll_to_date(self):
        """
        iterate through total_cost variable of invoices to find current
        total earned on a project
        """
        # To find the sum of all `payroll_cost` for a project instance
        # use self.invoice_set (the reverse name for the field with a fk)
        # aggregate the payroll_cost & get the sum of that.
        # that gives you a dictionary with the key as payroll_cost__sum
        # access that key to get total. Do same for other cost
        if self.invoice_set:
            payroll_agg = self.invoice_set.aggregate(models.Sum('labor_cost'))
            payroll = payroll_agg.get('labor_cost__sum', 0.00)
        payroll = 0
        return float(payroll)

    @property
    def other_cost_to_date(self):
        other_cost_agg = self.invoice_set.aggregate(models.Sum('other_cost'))
        other_cost = other_cost_agg.get('other_cost__sum', 0.00)
        other_cost = 0
        return float(other_cost)
    
    @property
    def total_invoiced(self):
        ''' Sum of `payroll_to_date` & 1other_cost_to_date1 ''' 
        self.payroll_to_date + self.other_cost_to_date
    @property
    def total_budget(self):
        ''' Sum of payroll and other cost budgets '''
        return self.other_cost_budget + self.payroll_budget

    @property
    def inspector_hours_to_date(self):
        st= self.invoice_set.aggregate(models.Sum('straight_hours'))
        straight_hours = st.get('straight_hours__sum', 0.0)
        ot = self.invoice_set.aggregate(models.Sum('overtime_hours'))
        overtime_hours = st.get('overtime_hours__sum', 0.0)
        return float(straight_hours + overtime_hours)

    @property
    def last_invoiced(self):
        """
        return the end date on the most recent invoice instance
        """
        if self.invoice_set is None:
            return self.start_date.strftime("%m/%d/%y")
        latest_invoice = self.invoice_set.latest('end_date')
        return latest_invoice.end_date.strftime("%m/%d/%Y")

    @property
    def end_date(self):
        """
        return date of last invoice date for completed jobs or 'present' for
        jobs that are still active.
        """
        if self.active:
            return "present"
        if self.invoice_set is None:
            return "unknown"
        latest_invoice = self.invoice_set.latest('end_date')
