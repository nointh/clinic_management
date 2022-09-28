from django.urls import path

from prescription.views import PdfView, PrescriptionCreateView, PrescriptionDeleteView, PrescriptionDetailView, PrescriptionEditView, PrescriptionListView, PrescriptionPdfView
app_name='prescription'
urlpatterns = [
    path('', PrescriptionListView.as_view(), name='index'),
    path('create', PrescriptionCreateView.as_view(), name='create'),
    path('<int:pk>', PrescriptionDetailView.as_view(), name='detail'),
    path('<int:pk>/edit', PrescriptionEditView.as_view(), name='edit'),
    path('<int:pk>/delete', PrescriptionDeleteView.as_view(), name='delete'),
    path('<int:pk>/pdf', PrescriptionPdfView.as_view(), name='print'),
    path('<int:pk>/pdfview', PdfView.as_view(), name='viewPrint'),
]

