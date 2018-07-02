from .models import Project
from rest_framework import serializers

class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ('prudent_number', 'penndot_number', 'last_invoiced', 'budget_utilization')