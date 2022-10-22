from datetime import datetime
from django.shortcuts import render
from django.views import View
from django.db.models import Count, Sum, Avg, FloatField
from django.db.models.functions import Coalesce

from base.views import LoginRequiredView
from clinic_management.models import Invoice, Medicine, MedicineType, Patient, Prescription


class HomeView(View):
    def get(self, request):
        patient_count = Patient.objects.all()\
            .aggregate(patient_count = Count('id'))\
            ['patient_count']

        today_new_patient_count = Patient.objects.filter(created_at__date=datetime.now())\
            .aggregate(patient_count = Count('id'))\
            ['patient_count']
        
        medicine_count = Medicine.objects.all()\
            .aggregate(medicine_count = Count('id'))\
            ['medicine_count']

        medicine_type_count = MedicineType.objects.all()\
            .aggregate(medicine_type_count = Count('id'))\
            ['medicine_type_count']

        prescription_count = Prescription.objects.all()\
            .aggregate(prescription_count = Count('id'))\
            ['prescription_count']

        today_new_prescription_count = Prescription.objects.filter(created_at__date=datetime.now())\
            .aggregate(prescription_count = Count('id'))\
            ['prescription_count']

        invoice_count = Invoice.objects.all()\
            .aggregate(invoice_count = Count('id'))\
            ['invoice_count']

        today_invoice_count_and_total = Invoice.objects.all()\
            .aggregate(invoice_count = Count('id'), invoice_total = Coalesce(Sum('total'), 0, output_field=FloatField()))

        top_paid_patient = Patient.objects.all()\
            .annotate(total = Coalesce(Sum('invoice__total'), 0, output_field=FloatField()))\
            .values('id', 'name', 'total')[:3]
        
        context = {
            'patient_count': patient_count,
            'medicine_count': medicine_count,
            'medicine_type_count': medicine_type_count,
            'prescription_count': prescription_count,
            'invoice_count': invoice_count,
            'today_invoice_count': today_invoice_count_and_total['invoice_count'],
            'today_invoice_total': today_invoice_count_and_total['invoice_total'],
            'top_paid_patient': top_paid_patient,
            'today_new_patient_count': today_new_patient_count,
            'today_new_prescription_count': today_new_prescription_count,
        }
        return render(request, 'home.html', context)