from collections import defaultdict
from datetime import datetime, timedelta
from clinic_management.models import Prescription, Invoice, InvoiceDetail
from django.db.models import Count, Sum, Avg
from itertools import chain 
from django.db.models.functions import ExtractMonth, ExtractYear

class ReportService:
    @staticmethod
    def get_general_report_by_date( from_date_range=datetime.now(), to_date_range=datetime.now()):
        invoice = Invoice.objects.filter(created_at__date__gte = from_date_range, created_at__date__lte = to_date_range)\
            .values('created_at__date')\
            .annotate(total = Sum('total')).annotate(invoice_count = Count('id'))\
            .values('created_at__date', 'invoice_count', 'total')
        prescription = Prescription.objects.filter(created_at__date__gte = from_date_range, created_at__date__lte = to_date_range)\
            .values('created_at__date')\
            .annotate(prescription_count = Count('id'))\
            .values('created_at__date', 'prescription_count')
        invoice_dict = {x['created_at__date']: { field: x.get(field, 0) for field in x.keys() } for x in invoice}
        prescription_dict = {x['created_at__date']: { field: x.get(field, 0) for field in x.keys() } for x in prescription}
        print(invoice_dict)
        print(prescription_dict)
        data = defaultdict(lambda: { 'invoice_count': 0, 
        'prescription_count':0,
        'total':0})
        for key in invoice_dict:
            print(key)
            for field in invoice_dict[key]:
                print(field)
                data[key][field] = invoice_dict[key][field]
        for key in prescription_dict:
            print(key)
            for field in prescription_dict[key]:
                print(field)
                data[key][field] = prescription_dict[key][field]

        return list(data.values())

    def get_general_report_by_month(self, from_date_range=datetime.now(), to_date_range=datetime.now()):
        invoice = Invoice.objects.filter(created_at__date__gte = from_date_range, created_at__date__lte = to_date_range)\
            .annotate(month=ExtractMonth('created_at'),year=ExtractYear('created_at'),) \
            .order_by() \
            .values('month', 'year')\
            .annotate(total = Sum('total')).annotate(invoice_count = Count('id'))\
            .values('month', 'year', 'invoice_count', 'total')
        prescription = Prescription.objects.filter(created_at__date__gte = from_date_range, created_at__date__lte = to_date_range)\
            .annotate(month=ExtractMonth('created_at'),year=ExtractYear('created_at'),) \
            .order_by() \
            .values('month', 'year')\
            .annotate(prescription_count = Count('id'))\
            .values('month', 'year', 'prescription_count')
        invoice_dict = {f"{x['month']}-{x['year']}" : { field: x.get(field, 0) for field in x.keys() } for x in invoice}
        prescription_dict = {f"{x['month']}-{x['year']}": { field: x.get(field, 0) for field in x.keys() } for x in prescription}
        print(invoice_dict)
        print(prescription_dict)
        data = defaultdict(lambda: { 'invoice_count': 0, 
        'prescription_count':0,
        'total':0})
        for key in invoice_dict:
            print(key)
            data[key]['month'] = key
            data[key]['invoice_count'] = invoice_dict[key]['invoice_count']
            data[key]['total'] = invoice_dict[key]['total']

        for key in prescription_dict:
            data[key]['month'] = key
            data[key]['prescription_count'] = prescription_dict[key]['prescription_count']

        return list(data.values())

    def get_general_report_by_year(self, from_date_range=datetime.now(), to_date_range=datetime.now()):
        invoice = Invoice.objects.filter(created_at__date__gte = from_date_range, created_at__date__lte = to_date_range)\
            .annotate(year=ExtractYear('created_at'),) \
            .order_by() \
            .values('year')\
            .annotate(total = Sum('total')).annotate(invoice_count = Count('id'))\
            .values('year', 'invoice_count', 'total')
        prescription = Prescription.objects.filter(created_at__date__gte = from_date_range, created_at__date__lte = to_date_range)\
            .annotate(year=ExtractYear('created_at'),) \
            .order_by() \
            .values('year')\
            .annotate(prescription_count = Count('id'))\
            .values('year', 'prescription_count')
        invoice_dict = {x['year']: { field: x.get(field, 0) for field in x.keys() } for x in invoice}
        prescription_dict = {x['year']: { field: x.get(field, 0) for field in x.keys() } for x in prescription}
        print(invoice_dict)
        print(prescription_dict)
        data = defaultdict(lambda: { 'invoice_count': 0, 
        'prescription_count':0,
        'total':0})
        for key in invoice_dict:
            print(key)
            data[key]['year'] = str(key)
            data[key]['invoice_count'] = invoice_dict[key]['invoice_count']
            data[key]['total'] = invoice_dict[key]['total']
        for key in prescription_dict:
            print(key)
            data[key]['year'] = str(key)
            data[key]['prescription_count'] = prescription_dict[key]['prescription_count']

        return list(data.values())

    def get_revenue_data(self, from_date_range=datetime.now(), to_date_range=datetime.now()):
        invoice = Invoice.objects.filter(created_at__date__gte = from_date_range, created_at__date__lte = to_date_range)\
            .order_by('created_at__date')\
            .values('created_at__date')\
            .annotate(total = Sum('total')).annotate(invoice_count = Count('id'))\
            .values('created_at__date', 'invoice_count', 'total')
        return invoice


    def get_revenue_chart_data_by_date(self, from_date_range=datetime.now(), to_date_range=datetime.now()):
        invoices = list(self.get_revenue_data(from_date_range, to_date_range))
        print(invoices)
        latest_invoice_date = from_date_range
        oldest_invoice_date = to_date_range
        date_dict = defaultdict(lambda: 0)
        for invoice in invoices:
            if datetime.combine(invoice["created_at__date"], datetime.min.time()) > datetime.combine(latest_invoice_date.date(), datetime.min.time()):
                latest_invoice_date = datetime.combine(invoice["created_at__date"], datetime.min.time())
            if datetime.combine(invoice["created_at__date"], datetime.min.time()) < datetime.combine(oldest_invoice_date.date(), datetime.min.time()):
                oldest_invoice_date = datetime.combine(invoice["created_at__date"], datetime.min.time())
            date_dict[datetime.strftime(invoice["created_at__date"], '%Y-%m-%d')] = invoice["total"]
        result_list = []
        print(oldest_invoice_date)
        print(latest_invoice_date)
        current_date = oldest_invoice_date
        while (current_date <= (latest_invoice_date + timedelta(days=1))):
            if datetime.strftime(current_date, '%Y-%m-%d') in date_dict.keys():
                result_list.append({'created_at__date': datetime.combine(current_date.date(), datetime.min.time()), 'total': date_dict[current_date.strftime('%Y-%m-%d')]})
            else:
                result_list.append({'created_at__date': datetime.combine(current_date.date(), datetime.min.time()), 'total': 0})
            current_date = current_date + timedelta(days=1)
        print(result_list)
        return result_list
        
    def get_revenue_chart_data_by_month(self, from_date_range=datetime.now(), to_date_range=datetime.now()):
        
        invoices = Invoice.objects.filter(created_at__date__gte = from_date_range, created_at__date__lte = to_date_range)\
            .annotate(month=ExtractMonth('created_at'),year=ExtractYear('created_at'),) \
            .order_by() \
            .values('month', 'year')\
            .annotate(total = Sum('total'))\
            .values('month', 'year', 'total')
        invoices = list(invoices)
        print(invoices)
        latest_invoice_month = 0
        latest_invoice_year = 0
        oldest_invoice_year = datetime.now().year
        oldest_invoice_month = datetime.now().month
        date_dict = defaultdict(lambda: 0)
        for invoice in invoices:
            if invoice['year'] > latest_invoice_year:
                latest_invoice_year = invoice['year']
                latest_invoice_month = invoice['month']
                print('uupdate latest month + year')
            elif invoice['year'] == latest_invoice_year and invoice['month'] > latest_invoice_month:
                latest_invoice_month = invoice['month']
                print('uupdate latest month ')

            if invoice['year'] < oldest_invoice_year:
                oldest_invoice_month = invoice['month']
                oldest_invoice_year = invoice['year']
                print('uupdate oldest month + year')
            elif  invoice['year']  == oldest_invoice_year and invoice['month'] < oldest_invoice_month:
                oldest_invoice_month = invoice['month']
                print('uupdate olde month ')
            date_dict[str(invoice['month']) + '-' + str(invoice['year'])] = invoice["total"]
        print(date_dict)
        result_list = []
        current_month = oldest_invoice_month
        current_year = oldest_invoice_year
        print(oldest_invoice_month)
        print(oldest_invoice_year)
        print(latest_invoice_month)
        print(latest_invoice_year)
        while current_year <= latest_invoice_year and current_month <= latest_invoice_month:
            month_str = str(invoice['month']) + '-' + str(invoice['year'])
            if month_str in date_dict.keys():
                print('case 1', month_str)
                result_list.append({'month': month_str, 'total': date_dict[month_str]})
            else:
                print('case 2', month_str)

                result_list.append({'month': month_str, 'total': 0})
            current_month += 1
            if current_month > 12:
                current_month = 1
                current_year += 1
            else:
                current_year += 1
        print(result_list)
        return result_list

    def get_revenue_chart_data_by_year(self, from_date_range=datetime.now(), to_date_range=datetime.now()):
        
        invoices = Invoice.objects.filter(created_at__date__gte = from_date_range, created_at__date__lte = to_date_range)\
            .annotate(year=ExtractYear('created_at'),) \
            .order_by() \
            .values('year')\
            .annotate(total = Sum('total'))\
            .values('year', 'total')
        invoices = list(invoices)
        print(invoices)
        latest_invoice_year = 0
        oldest_invoice_year = datetime.now().year
        date_dict = defaultdict(lambda: 0)
        for invoice in invoices:
            if invoice['year'] > latest_invoice_year:
                latest_invoice_year = invoice['year']

            if invoice['year'] < oldest_invoice_year:
                oldest_invoice_year = invoice['year']
            date_dict[str(invoice['year'])] = invoice["total"]
        print(date_dict)
        result_list = []
        current_year = oldest_invoice_year
        print(oldest_invoice_year)
        print(latest_invoice_year)
        while current_year <= latest_invoice_year:
            if str(current_year) in date_dict.keys():
                result_list.append({'year': str(current_year), 'total': date_dict[str(current_year)]})
            else:
                result_list.append({'year': str(current_year), 'total': 0})
            current_year += 1
        return result_list

    def get_medicine_report_data(self, from_date_range=datetime.now(), to_date_range=datetime.now()):
        medicine = InvoiceDetail.objects\
            .filter(invoice__created_at__date__gte = from_date_range, invoice__created_at__date__lte = to_date_range)\
            .values('medicine')\
            .annotate(total = Sum('line_total'), count=Count('medicine'))\
            .values('medicine__id', 'medicine__name', 'medicine__unit', 'total', 'count')
        return medicine

