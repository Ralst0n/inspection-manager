from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.db import models
from .models import Project, Invoice
from manager.inspectors.models import Inspector

# Register your models here.
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        """
        filter which projects show in list view
        """
        groups = []
        for group in request.user.groups.all():
            groups.append(str(group))
        if request.user.is_superuser:
            return Project.objects.all()
            return project
        else:
            return Project.objects.all().filter(office__in=groups)
    list_display = ('penndot_number', 'prudent_number', 'name')
    filter_horizontal = ('inspector',)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        """
        filter which projects show in list view
        """
        groups = []
        for group in request.user.groups.all():
            groups.append(str(group))
        if request.user.is_superuser:
            return Invoice.objects.all().filter(project__completed=False)
            return project
        else:
            return Invoice.objects.all().filter(project__office__in=groups).filter(project__completed=False)
    #project = Project.objects.filter(completed__isnull=False)
    list_display = ('project', 'estimate_number')
    list_filter = ('project',)
