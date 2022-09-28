from django.urls import path
from .views import PatientCreateView, PatientDeleteView, PatientDetailView, PatientEditView, PatientListView, PatientDetailView, edit_patient, get_all_patients, detail, create_patient, test_form
app_name = 'patient'
urlpatterns = [
    path('', PatientListView.as_view(), name='index'),
    path('<int:pk>', PatientDetailView.as_view(), name="detail"),
    path('create', PatientCreateView.as_view(), name="create"),
    path('<int:pk>/delete', PatientDeleteView.as_view(), name="delete"),
    path('<int:pk>/edit', PatientEditView.as_view(), name="edit"),
    # path('testform', test_form, name="testform"),
]