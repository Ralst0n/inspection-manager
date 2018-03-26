from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.EquipmentListView.as_view(), name="equipment"),
    url(r'^(?P<pk>\d+)', views.EquipmentDetailView.as_view(), name="equipment-detail"),
    url(r'^create$', views.EquipmentCreateView.as_view(), name='equipment-create'),
    url(r'^update/(?P<pk>\d+)$', views.EquipmentUpdateView.as_view(), name='equipment-update'),
]
