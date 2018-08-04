from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
# Create your views here.

from apps.invoices.models import Invoice
from apps.projects.models import Project

class DashboardView(LoginRequiredMixin, ListView):
    template_name = "dashboard.html"
    
    def idk(self):
        if self.request.user.profile.role == "Observer":
            redirect('/invoices/list')
    def get_queryset(self):
        # If the user is a creator, the data wil be invoices they created that aren't finalized
        # if the user is a manager or reviewer, the data will be their queue of invoices to chcek
        user_role = self.request.user.profile.role

        if user_role == "Preparer":
            qs = Invoice.objects.filter(creator=self.request.user).filter(status__lte=0)
        elif user_role == "Manager":
            qs = Invoice.objects.filter(creator__profile__office=self.request.user.profile.office).filter(status=1)
        elif user_role == "Reviewer":
            qs = Invoice.objects.filter(status=2)
        else:
            qs = []
        
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_role = self.request.user.profile.role
        if user_role == "Preparer" or user_role == "Manager":
            # Show most recent activity on last 7 invoices that wasn't done by this person
            context['recent'] = Invoice.objects.filter(
            creator__profile__office=self.request.user.profile.office).exclude(last_modified_by=self.request.user).order_by(
                '-last_modified')[:7]
            # Additionally show revenue status for preparers and managers.
            total = 0
            for project in Project.objects.all():
                total += project.ytd_invoiced
            context['revenue'] = total
            context['revenue_percent'] = (total/1000000) * 100
        else:
            context['recent'] = Invoice.objects.filter(
            creator__profile__office=self.request.user.profile.office).order_by(
                'last_modified')[:7]
        return context

    