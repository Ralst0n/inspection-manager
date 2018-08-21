from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max, Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.views import generic

from datetime import timedelta
from rest_framework import generics, viewsets
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

from .models import Project
from .serializers import ProjectSerializer 
from apps.invoices.models import Invoice

# Create your views here.

@login_required
def all_projects(request):
    groups = []
    for group in request.user.groups.all():
        groups.append(str(group))
    project_list = Project.objects.all().filter(office__in=groups)
    return render(request, 'all_project_list.html',
    {
    'project_list': project_list,
    })

class ProjectSearchView(LoginRequiredMixin, generic.ListView):
    model = Project
    template_name = 'all_project_list.html'

    def get_queryset(self):
        office = self.request.user.profile.office
        return Project.objects.filter(office=office)

class ProjectsListView(LoginRequiredMixin, generic.ListView):
    model = Project
    def get_queryset(self):
        """
        filter which projects show in list view
        """
        office = self.request.user.profile.office
        groups = []
        for group in self.request.user.groups.all():
            groups.append(str(group))
        return Project.objects.filter(office=office).filter(completed__exact=False)

class ProjectsDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # self.object gives you access to the object the detail page is for.
        context['invoices'] = Invoice.objects.filter(project=self.object, status__gte=1).order_by('-end_date')
        return context

    def get_object(self):
        _object = Project.objects.get(pk=self.kwargs['pk'])
        if _object.office != self.request.user.profile.office:
            return {}
        else:
            return _object

class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows projects to be viewed or edited.
    """
    queryset = Project.objects.all().order_by('prudent_number')
    serializer_class = ProjectSerializer

class ProjectDetail(generics.RetrieveUpdateAPIView):
    queryset = Project.objects.all()
    render_classes = (JSONRenderer,)

def get_info(request):
    '''Get the information to auto populate the estimate number and start date for an invoice'''
    prudent_number = request.POST.get("prudent_number")
    project = Project.objects.get(prudent_number=prudent_number)
    # if there are no previous invoices, tell js there's no previous data.
    if project.invoice_set.count() == 0:
        start_date = project.start_date.strftime("%Y-%m-%d")
        data = {
            "estimate_number": 1,
            "start_date": start_date

        }
    else:
        latest_invoice = project.invoice_set.latest('end_date')
        estimate_number = latest_invoice.estimate_number + 1
        start_date = latest_invoice.end_date + timedelta(days=1)
        start_date = start_date.strftime("%Y-%m-%d")
        data = {
            "previous": True,
            "estimate_number": estimate_number,
            "start_date": start_date
        }

    return JsonResponse(data)