from django.urls import path
from .views import MedicineDetaiView, MedicineListView, MedicineValidationFormView


app_name = 'api'
urlpatterns = [
    path('medicine', MedicineListView.as_view(), name='medicine_list'),
    path('medicine/<int:id>', MedicineDetaiView.as_view(), name='medicine_detail'),
    path('medicine/validate', MedicineValidationFormView.as_view(), name='medicine_validation')

]

