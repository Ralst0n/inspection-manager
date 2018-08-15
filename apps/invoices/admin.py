from django.contrib import admin
from .models import Invoice, Comments
# Register your models here.
# admin.site.register(Invoice)
class CommentInline(admin.TabularInline):
    model = Comments
    extra = 1

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('project', 'estimate_number', 'status')
    list_filter = ('project', 'status')
    inlines = [CommentInline]

admin.site.register(Invoice, InvoiceAdmin)
