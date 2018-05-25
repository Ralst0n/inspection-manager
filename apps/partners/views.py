from django.views.generic import DetailView, ListView
from .models import LetProject, ProjectTeam, BusinessPartner
from django.contrib.auth.mixins import LoginRequiredMixin


class LetProjectList(ListView):
    def get_queryset(self):
        # People of the office should only see their invoices that are not yet approved
        queryset = LetProject.objects.all()
            
        return queryset
    template_name = "letproject_list.html"
    # Set the name to be used in the template to access object list
    context_object_name = "letprojects"

class LetProjectView(LoginRequiredMixin, DetailView):
    model = LetProject

    template_name = 'letproject_details.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['winning_subs'] = ProjectTeam.objects.filter(agreement_number=self.object).filter(prime=self.object.winner)
        context['second_subs'] = ProjectTeam.objects.filter(agreement_number=self.object).filter(prime=self.object.second_place)
        context['third_subs'] = ProjectTeam.objects.filter(agreement_number=self.object).filter(prime=self.object.third_place)
        return context