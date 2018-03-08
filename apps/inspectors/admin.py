from django.contrib import admin
from .models import Inspector, Notes
# Register your models here.
admin.site.register(Notes)


@admin.register(Inspector)
class InspectorAdmin(admin.ModelAdmin):
    model = Inspector
    list_display = ('first_name', 'last_name', 'classification')
