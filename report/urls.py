from django.urls import path

from report.views import GeneralReportView, MedicineReportView, RevenueChartView
app_name = 'report'
urlpatterns = [
    path('', GeneralReportView.as_view(), name='general'),
    path('revenue', RevenueChartView.as_view(), name='revenue'),
    path('medicine', MedicineReportView.as_view(), name='medicine'),
]