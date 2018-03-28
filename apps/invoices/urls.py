
from django.urls import path

from . import views

app_name = 'invoices'
urlpatterns = [
    path('', views.InvoiceList.as_view(), name='invoices'),
    path('<pk>/', views.InvoiceView.as_view(), name='details'),
    path('new', views.invoice_new, name='invoice_new'),
    path('edit/<pk>/', views.invoice_edit, name='invoice_edit'),
    path('submit/<pk>/', views.invoice_submit, name='invoice_submit'),
    path('reject/<pk>/', views.invoice_reject, name='invoice_reject'),
    path('inv_number/<pk>/', views.invoice_number, name='invoice_number'),
]