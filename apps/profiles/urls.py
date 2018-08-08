
from django.urls import path

from . import views

app_name = 'profiles'
urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('guest', views.guest_log, name="guest")
]