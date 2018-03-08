from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.ProjectsListView.as_view(), name='projects'),
    url(r'^search/$', views.ProjectSearchView.as_view(), name='search-projects'),
    url(r'^(?P<pk>\d{3}.\d{3})', views.ProjectsDetailView.as_view(), name='project-detail'),
]
