from django.contrib import admin
from .models import Invoice, Comments
# Register your models here.
# admin.site.register(Invoice)

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('project', 'estimate_number', 'status')
    list_filter = ('project', 'status')
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Comments)