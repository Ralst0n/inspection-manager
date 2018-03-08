from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views import generic

from .models import Equipment

# Create your views here.
class EquipmentListView(LoginRequiredMixin, generic.ListView):
    model = Equipment
    def get_queryset(self):
        """
        filter which projects show in list view
        """
        return Equipment.objects.filter(office=self.request.user.profile.office)

class EquipmentDetailView(LoginRequiredMixin, generic.DetailView):
    model = Equipment

    def get_object(self):
        _object = Equipment.objects.get(pk=self.kwargs['pk'])
        if _object.office != self.request.user.profile.office:
            return {}
        else:
            return _object
