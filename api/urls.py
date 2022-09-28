from django.urls import path
from .views import MedicineDetaiView, MedicineListView


app_name = 'api'
urlpatterns = [
    path('medicine', MedicineListView.as_view(), name='medicine_list'),
    path('medicine/<int:id>', MedicineDetaiView.as_view(), name='medicine_detail')   
]

