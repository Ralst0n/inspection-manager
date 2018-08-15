from django.contrib import admin
from .models import Inspector, Notes, History
# Register your models here.

class NoteInline(admin.TabularInline):
    model = Notes
    extra = 1

class HistoryInline(admin.TabularInline):
    model = History
    extra = 0

@admin.register(Inspector)
class InspectorAdmin(admin.ModelAdmin):
    model = Inspector
    list_display = ('first_name', 'last_name', 'classification')
    inlines = [HistoryInline, NoteInline]