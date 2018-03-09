from django.shortcuts import redirect, render
from django.views.generic.list import ListView
# Create your views here.

from apps.invoices.models import Invoice

class DashboardView(ListView):
    template_name = "dashboard.html"
    
    def idk(self):
        if self.request.user.profile.role == "Observer":
            redirect('/invoices/list')
    def get_queryset(self):
        # If the user is a creator, the data wil be invoices they created that aren't finalized
        # if the user is a manager or reviewer, the data will be their queue of invoices to chcek
        user_role = self.request.user.profile.role

        if user_role == "Preparer":
            qs = Invoice.objects.filter(creator=self.request.user).filter(status__lte=2)
        elif user_role == "Manager":
            qs = Invoice.objects.filter(creator__profile__office=self.request.user.profile.office).filter(status=1)
        elif user_role == "Reviewer":
            qs = Invoice.objects.filter(status=2)
        else:
            qs = Invoice.objects.all()
        
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_role = self.request.user.profile.role
        if user_role == "Preparer":
            context['recent'] = Invoice.objects.filter(
            creator__profile__office=self.request.user.profile.office).filter(status__gt=1).order_by(
                '-last_modified')[:10]
        elif user_role == "Manager":
            context['recent'] = Invoice.objects.filter(
            creator__profile__office=self.request.user.profile.office).filter(status__gt=2).order_by(
                '-last_modified')[:10]
        return context

    