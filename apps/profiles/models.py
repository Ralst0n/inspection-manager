from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    OFFICE = (
        ('King of Prussia', 'KOP'),
        ('Pittsburgh', 'PGH'),
        ('Syracuse', 'SYR'),
    )
    ROLE = (
        ('Preparer','Preparer' ),
        ('Manager','Manager'),
        ('Reviewer','Reviewer'),
        ('Observer','Observer'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    office = models.CharField(choices=OFFICE, default='King of Prussia', max_length=30)
    role = models.CharField(choices=ROLE, default='Observer', max_length=30)
    receive_newsletter = models.BooleanField(default=True, verbose_name="Would you like to receive notification emails?")
    
    def __str__(self):
        return self.user.username
    @property
    def display_name(self):
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name[0].upper()}.{self.user.last_name.capitalize()}"
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
 

class Scrape(models.Model):
    date = models.DateField(auto_now=True)
