from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic.list import ListView

from datetime import date, datetime
from rq import Queue
from worker import conn

from .models import Scrape
from apps.inspectors.tasks import scrape_let_projects, scrape_planned_projects
from apps.invoices.models import Invoice
from apps.projects.models import Project

def monthly_invoices(year=datetime.now().year):
    # create list of revenue for each month
    revenue_list = [0]*12
    # for each month grab all invoices with end dates with that month
    for month in range(1,13):
        for invoice in Invoice.objects.filter(end_date__year=year, end_date__month=month):
            # add invoice total to revenue index corresponding to its month
            revenue_list[month-1] += invoice.total_cost
    return revenue_list


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

        if self.request.user.is_superuser:
            # Don't run if it's already run that day
            if Scrape.objects.count() >= 1  and Scrape.objects.last().date >= date.today():
                pass
            else: 
                q = Queue(connection=conn)
                q.enqueue(scrape_let_projects)
                q.enqueue(scrape_planned_projects)
                Scrape.objects.create()

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

def guest_log(request):
    user = User.objects.get(username="Guest")
    login(request, user)
    return redirect('/')

def chart_revenues(request):
    revenue_list = monthly_invoices()
    previous_list = monthly_invoices(datetime.now().year-1)
    data = {
        "revenue": revenue_list,
        "previous": previous_list
    }
    return JsonResponse(data)
