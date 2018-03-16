from django.urls import path

from apps.inspectors import views

from django.conf.urls import url
urlpatterns = [
    url(r'^$', views.InspectorListView.as_view(), name='inspectors'),
    url(r'dashboard$', views.index, name='index'),
    url(r'^search', views.InspectorSearchView.as_view(), name='search-inspectors'),
    url(r'^(?P<pk>\d+)$', views.InspectorDetailView.as_view(), name='inspector-detail'),
    url(r'^create$', views.InspectorCreateView.as_view(), name='inspector-create'),
    url(r'^update/(?P<pk>\d+)$', views.InspectorUpdateView.as_view(), name='inspector-update'),
    path('scrape_projects', views.ScrapeProjects,),
]
