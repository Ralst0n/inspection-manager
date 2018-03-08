from django.contrib import admin
from .models import Invoice, Comments
# Register your models here.
# admin.site.register(Invoice)

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'status')
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Comments)