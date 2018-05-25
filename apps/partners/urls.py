from django.urls import path

from apps.partners import views

app_name='letproject'
urlpatterns = [
    path('', views.LetProjectList.as_view(),),
    path('<pk>', views.LetProjectView.as_view(), name='details'),
]