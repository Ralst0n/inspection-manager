from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import render
from django.views import generic

from .models import Project, Invoice

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
        # return Project.objects.filter(completed__exact=False).filter(office__in=groups)
        return Project.objects.filter(office=office).filter(completed__exact=False)

class ProjectsDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # self.object gives you access to the object the detail page is for.
        context['invoices'] = Invoice.objects.filter(project=self.object).order_by('-end_date')
        return context

    def get_object(self):
        _object = Project.objects.get(pk=self.kwargs['pk'])
        if _object.office != self.request.user.profile.office:
            return {}
        else:
            return _object
