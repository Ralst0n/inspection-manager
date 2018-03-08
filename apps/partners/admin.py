from django.contrib import admin
from .models import BusinessPartner, LetProject, PlannedProject, ProjectTeam
# Register your models here.
admin.site.register(LetProject)
admin.site.register(PlannedProject)
admin.site.register(BusinessPartner)
admin.site.register(ProjectTeam)
