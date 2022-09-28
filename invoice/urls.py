from django.urls import path
from invoice.views import InvoiceDeleteView, InvoiceListView, InvoiceCreateView, InvoiceDetailView, InvoiceEditView
app_name = 'invoice'

urlpatterns = [
    path('', InvoiceListView.as_view(), name='index'),
    path('create', InvoiceCreateView.as_view(), name='create'),
    path('<int:pk>', InvoiceDetailView.as_view(), name='detail'),
    path('<int:pk>/edit', InvoiceEditView.as_view(), name='edit'),
    path('<int:pk>/delete', InvoiceDeleteView.as_view(), name='delete'),

]