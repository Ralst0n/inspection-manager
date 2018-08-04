from django.conf.urls import include, url
from django.urls import path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'api', views.ProjectViewSet)

urlpatterns = [
    url(r'^$', views.ProjectsListView.as_view(), name='projects'),
    url(r'^search/$', views.ProjectSearchView.as_view(), name='search-projects'),
    url(r'^(?P<pk>\d{3}.\d{3})', views.ProjectsDetailView.as_view(), name='project-detail'),
    path("get_info", views.get_info),
]

urlpatterns += router.urls
