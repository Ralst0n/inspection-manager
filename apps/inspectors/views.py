from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User, Group
from django.db.models import Q, Sum
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic

from datetime import date, datetime, timedelta
from decimal import Decimal
from rq import Queue
from worker import conn

from .models import History, Inspector, Notes
from .newsletters import check_project_burnrate, check_inspector_certs
from .tasks import email_news_letter, scrape_let_projects, scrape_planned_projects
from apps.invoices.models import Invoice
from apps.projects.models import Project
from apps.utils.helpers import formatted_date


# Create your views here.
q = Queue(connection=conn)
@login_required
def index(request):
    groups = []
    for group in request.user.groups.all():
        groups.append(str(group))
    inspectors = Inspector.objects.all().filter(office__in=groups).order_by('-id')[:7]
    num_inspectors = Inspector.objects.filter(office__in=groups).count()
    num_prudent_inspectors = Inspector.objects.filter(is_employee__exact=True).filter(office__in=groups).count()
    projects = Project.objects.all().filter(office__in=groups).filter(completed=False).order_by('-start_date')
    num_projects = Project.objects.filter(office__in=groups).filter(completed=False).count()
    num_projects_unfilled = projects.filter(inspector__isnull=True).count()
    num_projects_filled = num_projects - num_projects_unfilled
    invoices = Invoice.objects.all().filter(project__office__in=groups).order_by('-id')[:7] #order by id so projects that are behind show up
    ytd = 0 #list(Invoice.objects.filter(end_date__year=datetime.now().year).filter(project__office__in=groups).aggregate(Sum('total_cost')).values())[0]
    if (ytd is None):
        ytd = 0
    fytd = ytd
    ytdofgoal = float(ytd/1000000)*100
    fytdofgoal = float(83.83/100)
    if ("Test" in groups):
        fytd += 1
        ytdofgoal = fytdofgoal
    percentageofgoal = "{}% of goal".format(round(ytdofgoal,2))
    return render(request, 'dashboard.html',
    {
    'inspectors':inspectors,
    'invoices': invoices,
    'num_inspectors':num_inspectors,
    'num_prudent_inspectors':num_prudent_inspectors,
    'num_projects': num_projects,
    'num_projects_filled':num_projects_filled,
    'percentageofgoal':percentageofgoal,
    'projects':projects,
    'ytd':ytd,
    'fytd':fytd,
    'fytdofgoal':fytdofgoal,
     })

class InspectorCreateView(generic.edit.CreateView):
    template_name = 'create_inspector.html'
    model = Inspector
    fields = '__all__'

class InspectorUpdateView(generic.edit.UpdateView):
    template_name = 'create_inspector.html'
    model = Inspector
    fields = '__all__'

class InspectorDelete(generic.edit.DeleteView):
    model = Inspector
    success_url = reverse_lazy('search-inspectors')
    
class InspectorSearchView(generic.ListView):
    template_name='all_inspector_list.html'

    def get_queryset(self):
        # Return information for any inspector that is a part of the requesting
        # user's office, or is a part of neither office.
        if self.request.user.is_authenticated:
            qs = Inspector.objects.filter(Q(office=self.request.user.profile.office)|
                                      Q(office='None'))
        else:
            qs = Inspector.objects.filter(office='None')

        return qs

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['inspector_count']=Inspector.objects.filter(
                                        Q(office=self.request.user.profile.office)|
                                        Q(office='None')).count()
        else:
            context['inspector_count']=Inspector.objects.filter(
                                        office='None').count()
        return context

class InspectorListView(LoginRequiredMixin, generic.ListView):
    template_name='inspector_list.html'
    model = Inspector
    def get_queryset(self):
        if self.request.user.is_anonymous:
            return []
        qs = Inspector.objects.filter(office=self.request.user.profile.office)
        return qs

class InspectorDetailView(
    LoginRequiredMixin, generic.DetailView
):
    redirect_field_name = "/search"
    model = Inspector

    def get_object(self):
        _object = Inspector.objects.get(pk=self.kwargs['pk'])
        # If the person works for the requesters office or is a 'free agent'
        # show their page with the information filled out
        if _object.office == self.request.user.profile.office or _object.office == 'None':
            return _object
        else:
            return 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # self.object gives you access to the object the detail page is for.
        context['notes'] = Notes.objects.filter(inspector=self.object).order_by('-created_at')
        context['history'] = History.objects.filter(inspector=self.object).order_by('-start_date')
        context['id'] = self.kwargs['pk']
        return context

@user_passes_test(lambda u: u.is_superuser)
def ScrapeProjects(request):
    result = q.enqueue(scrape_planned_projects)
    resp = "Projects should scrape..."
    return HttpResponse(resp)

@user_passes_test(lambda u: u.is_superuser)
def Newsletter(request):
    resp = email_news_letter()
    return HttpResponse(resp)

@user_passes_test(lambda u: u.is_superuser)
def LetProjects(request):
    resp = scrape_let_projects()
    return HttpResponse(resp)

@user_passes_test(lambda u: u.is_superuser)
def office_overview(request):
    projects = Project.objects.all()
    month = Invoice.objects.latest('end_date').end_date.month
    year = Invoice.objects.latest('end_date').end_date.year
    months_remaining = datetime(2018, 12, 1).month - month
    
    # GET TOTAL INVOICED FOR THE YEAR
    invoiced_to_date = 0
    
    for project in projects:
        invoiced_to_date += project.ytd_invoiced
    
    # GET TOTAL INVOICED FOR THE MONTH
    monthly_total = 0
    last_monthly_total = 0
    last_last_monthly_total = 0
    three_old_monthly_total = 0
    for invoice in Invoice.objects.filter(end_date__month=month).filter(status__gte=3):
        monthly_total += invoice.total_cost
    
    for invoice in Invoice.objects.filter(end_date__month=(month-1)).filter(status__gte=3):
        last_monthly_total += invoice.total_cost
    
    for invoice in Invoice.objects.filter(end_date__month=(month-2)).filter(status__gte=3):
        last_last_monthly_total += invoice.total_cost

    for invoice in Invoice.objects.filter(end_date__month=(month-3)).filter(status__gte=3):
        three_old_monthly_total += invoice.total_cost

    # REVENUE PROJECTION JUST TOTAL THIS MONTH TIMES MONTHS REMAINING PLUS TOTAL TO DATE
    # Actually just average the year thus far
    # revenue_projection = (months_remaining * monthly_total) + invoiced_to_date
    revenue_projection = (invoiced_to_date/month) * months_remaining + invoiced_to_date

    #BURN RATE RUSH
    ending_projects = []

    for project in Project.objects.filter(office="King of Prussia").filter(active=True):
        # Get the average amount of the last 3 invoices' labor cost
        invoice_set =  project.invoice_set.order_by("-end_date")[:3]
        # If there are no invoices, end this check
        if invoice_set.count() == 0:
            return ""
        # Get the total labor cost of last 3 invoices as a decimal
        last_3 = project.invoice_set.order_by("-end_date")[:3].aggregate(Sum('labor_cost'))
        # Get just the Decimal value from last_3
        burn_rate = list(last_3.values())[0]
        total_duration = 0        
        for invoice in invoice_set:
             total_duration += (invoice.end_date - invoice.start_date).days
        
        daily_avg = Decimal(burn_rate / total_duration)
        days_left = round(((project.payroll_budget) - project.payroll_to_date)/daily_avg)
        if days_left <= 120:
            end_project = formatted_date(project.get_last_invoiced() + timedelta(days=(days_left)))
            ending_projects.append([
                project.prudent_number, end_project, 'Specific Rate'
            ])
        # Repeat process for other cost 
        last_3 = project.invoice_set.order_by("-end_date")[:3].aggregate(Sum('other_cost'))
        burn_rate = list(last_3.values())[0]
        daily_avg = Decimal(burn_rate / total_duration)
        days_left = round((project.other_cost_budget - project.other_cost_to_date)/daily_avg)
        if days_left <= 120:
            end_project = formatted_date(project.get_last_invoiced() + timedelta(days=(days_left)))
            ending_projects.append([
                project.prudent_number, end_project, 'Other Cost'
            ])
    context = {
        'revenue_projection': revenue_projection,
        'end_dates': ending_projects,
        'monthly': monthly_total,
        'yearly': invoiced_to_date,
        'month': datetime(year, month, 1).strftime('%B'),
        'last_month': datetime(year, month -1, 1).strftime('%B'),
        'last_last_month': datetime(year, month-2, 1).strftime('%B'),
        'three_old_month': datetime(year, month-3, 1).strftime('%B'),
        'last_monthly': last_monthly_total,
        'last_last_monthly': last_last_monthly_total,
        'three_old_monthly': three_old_monthly_total,
        'year': year
    }

    return render(request, 'overview.html', context)

    
