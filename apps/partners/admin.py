from django.contrib import admin
from .models import BusinessPartner, LetProject, PlannedProject, ProjectTeam
# Register your models here.

class LetProjectAdmin(admin.ModelAdmin):
    list_display = ("agreement_number", "district", "winner", "let_date")
    list_filter = ("district", "let_date")
admin.site.register(LetProject, LetProjectAdmin)

class PlannedProjectAdmin(admin.ModelAdmin):
    list_display = ('agreement_number', 'scrapped_date', 'district')
admin.site.register(PlannedProject, PlannedProjectAdmin)

admin.site.register(BusinessPartner)
admin.site.register(ProjectTeam)
