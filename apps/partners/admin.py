from django.contrib import admin
from .models import BusinessPartner, LetProject, PlannedProject, ProjectTeam
# Register your models here.
admin.site.register(LetProject)

class PlannedProjectAdmin(admin.ModelAdmin):
    list_display = ('agreement_number', 'scrapped_date', 'district')
admin.site.register(PlannedProject, PlannedProjectAdmin)

admin.site.register(BusinessPartner)
admin.site.register(ProjectTeam)
