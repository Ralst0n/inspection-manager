from django.db import models
from django.shortcuts import reverse

from datetime import datetime

class PlannedProject(models.Model):
    agreement_number = models.CharField(max_length=6)
    district = models.DecimalField(max_digits=2, decimal_places=0)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    cost = models.CharField(max_length=30)
    office = models.CharField(max_length=50)
    url = models.URLField()
    advance_date = models.DateField()
    scrapped_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.agreement_number

class BusinessPartner(models.Model):
    name = models.CharField(max_length=255)
    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class LetProject(models.Model):
    agreement_number = models.CharField(max_length=6)
    district = models.DecimalField(max_digits=2, decimal_places=0)
    winner = models.ForeignKey('partners.BusinessPartner',
                                on_delete=models.CASCADE,
                                related_name='wins',
                                null = True)
    second_place = models.ForeignKey('partners.BusinessPartner',
                                    related_name='seconds', null=True,
                                    on_delete=models.CASCADE)
    third_place = models.ForeignKey('partners.BusinessPartner',
                                    related_name='thirds', null=True,
                                    on_delete=models.CASCADE)
    let_date = models.DateField(default="2017-12-31")
    scrapped_date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.agreement_number

    def get_absolute_url(self):
        """
        Returns the url to access a particular invoice.
        """
        return reverse('letproject:details', args=[self.id])

class ProjectTeam(models.Model):
    agreement_number = models.ForeignKey('partners.LetProject',
                                          on_delete=models.CASCADE
    )
    prime = models.ForeignKey('partners.BusinessPartner',
                                on_delete= models.CASCADE,
                                related_name = 'asPrime',
                                null = True
    )
    sub = models.ForeignKey('partners.BusinessPartner',
                                on_delete= models.CASCADE,
                                related_name = 'asSub',
                                null = True
    )

    def __str__(self):
        return f"{self.agreement_number}: {self.prime} & {self.sub}"
