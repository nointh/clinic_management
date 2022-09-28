from django.urls import path

from medicine.views import MedicineCreateView, MedicineDeleteView, MedicineDetailView, MedicineEditView, MedicineListView
app_name = 'medicine'
urlpatterns = [
    path('', MedicineListView.as_view(), name='index'),
    path('create', MedicineCreateView.as_view(), name='create'),
    path('<int:pk>/edit', MedicineEditView.as_view(), name='edit'),
    path('<int:pk>', MedicineDetailView.as_view(), name='detail'),
    path('<int:pk>/delete', MedicineDeleteView.as_view(), name='delete'),

]