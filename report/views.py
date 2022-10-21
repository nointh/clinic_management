from datetime import date, datetime, timedelta
from time import strftime
from django.shortcuts import render
from django.views import View
from django.utils import timezone
from django.db.models import Avg, Sum, Count
from report.services import ReportService
# Create your views here.
INITIAL_RANGE_DAYS = 5
class GeneralReportView(View):
    def get(self, request):
        now = datetime.strftime(datetime.now(), '%Y-%m-%d')
        to_date_range = datetime.strptime(request.GET.get('to', now), '%Y-%m-%d')
        from_date_range = datetime.strptime(request.GET.get('from', datetime.strftime(to_date_range - timedelta(days=INITIAL_RANGE_DAYS), '%Y-%m-%d')), '%Y-%m-%d')

        
        group_by = request.GET.get('by', 'date')
        if group_by == 'month':
            data = ReportService().get_general_report_by_month(from_date_range, to_date_range)
        elif group_by == 'year':
            data = ReportService().get_general_report_by_year(from_date_range, to_date_range)
        else:
            data = ReportService().get_general_report_by_date(from_date_range, to_date_range)
        context = {
            'from_date': from_date_range,
            'to_date': to_date_range,
            'data': data,
            'by': group_by
            
        }
        return render(request, 'report/general_report.html', context)

class RevenueChartView(View):
    def get(self, request):
        now = datetime.strftime(datetime.now(), '%Y-%m-%d')
        to_date_range = datetime.strptime(request.GET.get('to', now ), '%Y-%m-%d')

        from_date_range = datetime.strptime(request.GET.get('from', datetime.strftime(to_date_range - timedelta(days=INITIAL_RANGE_DAYS), '%Y-%m-%d') ), '%Y-%m-%d')
        group_by = request.GET.get('by', 'date')
        if group_by == 'month':
            data = ReportService().get_revenue_chart_data_by_month(from_date_range, to_date_range)
        elif group_by == 'year':
            data = ReportService().get_revenue_chart_data_by_year(from_date_range, to_date_range)
        else:
            data = ReportService().get_revenue_chart_data_by_date(from_date_range, to_date_range)

        context = {
            'from_date': from_date_range,
            'to_date': to_date_range,
            'data': data,
            'by': group_by
        }
        return render(request, 'report/revenue_chart.html', context)

class MedicineReportView(View):
    def get(self, request):
        now = datetime.strftime(datetime.now(), '%Y-%m-%d')
        to_date_range = datetime.strptime(request.GET.get('to', now), '%Y-%m-%d')
        from_date_range = datetime.strptime(request.GET.get('from', datetime.strftime(to_date_range - timedelta(days=INITIAL_RANGE_DAYS), '%Y-%m-%d')), '%Y-%m-%d')
        group_by = request.GET.get('by', 'date')
        data = ReportService().get_medicine_report_data(from_date_range, to_date_range)
        context = {
            'from_date': from_date_range,
            'to_date': to_date_range,
            'data': data,
            'by': group_by
        }
        return render(request, 'report/medicine_report.html', context)
