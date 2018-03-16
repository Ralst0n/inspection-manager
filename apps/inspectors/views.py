from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User, Group
from django.db.models import Q, Sum
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic

from datetime import datetime

from .models import Inspector, Notes
from apps.projects.models import Project
from apps.invoices.models import Invoice
from .tasks import email_news_letter, scrape_let_projects
# Create your views here.

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
        return context

@user_passes_test(lambda u: u.is_superuser)
def ScrapeProjects(request):
    return scrape_let_projects();

@user_passes_test(lambda u: u.is_superuser)
def newsletter(request):
    return email_news_letter();