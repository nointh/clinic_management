from django.urls import path
from clinic_management.views.patient_views import PatientCreateView, PatientListView, PatientDetailView, PatientEditView, PatientDeleteView
from clinic_management.views.medicine_views import MedicineListView, MedicineCreateView, MedicineDeleteView, MedicineDetailView, MedicineEditView
from clinic_management.views.invoice_views import InvoiceListView, InvoiceCreateView, InvoiceDeleteView, InvoiceDetailView, InvoiceEditView
from clinic_management.views.prescription_views import PrescriptionListView, PrescriptionCreateView, PrescriptionDeleteView, PrescriptionDetailView, PrescriptionEditView, PrescriptionPrintView
app_name = 'clinic_management'
urlpatterns = [
    # Patient Views URLs
    path('patient', PatientListView.as_view(), name='patient_index'),
    path('patient/<int:pk>', PatientDetailView.as_view(), name="patient_detail"),
    path('patient/create', PatientCreateView.as_view(), name="patient_create"),
    path('patient/<int:pk>/delete', PatientDeleteView.as_view(), name="patient_delete"),
    path('patient/<int:pk>/edit', PatientEditView.as_view(), name="patient_edit"),

    # Medicine Views URLs
    path('medicine', MedicineListView.as_view(), name='medicine_index'),
    path('medicine/<int:pk>', MedicineDetailView.as_view(), name="medicine_detail"),
    path('medicine/create', MedicineCreateView.as_view(), name="medicine_create"),
    path('medicine/<int:pk>/delete', MedicineDeleteView.as_view(), name="medicine_delete"),
    path('medicine/<int:pk>/edit', MedicineEditView.as_view(), name="medicine_edit"),

    # Invoice Views URLs
    path('invoice', InvoiceListView.as_view(), name='invoice_index'),
    path('invoice/<int:pk>', InvoiceDetailView.as_view(), name="invoice_detail"),
    path('invoice/create', InvoiceCreateView.as_view(), name="invoice_create"),
    path('invoice/<int:pk>/delete', InvoiceDeleteView.as_view(), name="invoice_delete"),
    path('invoice/<int:pk>/edit', InvoiceEditView.as_view(), name="invoice_edit"),

    # Prescription Views URLs
    path('prescription', PrescriptionListView.as_view(), name='prescription_index'),
    path('prescription/<int:pk>', PrescriptionDetailView.as_view(), name="prescription_detail"),
    path('prescription/create', PrescriptionCreateView.as_view(), name="prescription_create"),
    path('prescription/<int:pk>/delete', PrescriptionDeleteView.as_view(), name="prescription_delete"),
    path('prescription/<int:pk>/edit', PrescriptionEditView.as_view(), name="prescription_edit"),
    path('prescription/<int:pk>/print', PrescriptionPrintView.as_view(), name="prescription_print"),




]