from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from clinic_management.models import Medicine
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from clinic_management.forms.medicine_forms import MedicineCreateForm, MedicineTypeForm
from clinic_management.forms.patient_forms import PatientCreateUpdateForm

# Create your views here.
class MedicineListView(View):
    @method_decorator(csrf_exempt)
    def get(self, request):
        
        keyword = request.GET.get('keyword', '')
        type = request.GET.get('type')
        query_result = Medicine.objects.filter(name__contains=keyword, medicine_type__name__contains=keyword)
        if type != None:
            query_result = query_result.filter(medicine_type=type)
        dict_data = []
        for medicine in query_result:
            dict_data.append(
                {
                    'id': medicine.id,
                    'medicineName': medicine.name,
                    'medicineType': str(medicine.medicine_type)
                }
            )
        return JsonResponse(dict_data, safe=False)

class MedicineDetaiView(View):
    @method_decorator(csrf_exempt)
    def get(self, request, id):
        medicine = Medicine.objects.get(id=id)
        dictionary = {
            'id': medicine.id,
            'name': medicine.name, 
            'stock_quantity': medicine.stock_quantity,
            'unit': medicine.unit ,
            'usage': medicine.usage,
            'orgin_price': medicine.origin_price,
            'sale_price': medicine.sale_price,
            'dosage': medicine.dose_per_day
            }
        print(dictionary)
        return JsonResponse(dictionary, safe=False)
class MedicineValidationFormView(View):
    form_class = MedicineCreateForm
    # template_name = "webapp/contact.html"
    # success_url = "/success/"

    def post(self, request, *args, **kwargs):
        if "__field_name__" in request.POST:
            return self.validate_field(request)
        return HttpResponse()

    def validate_field(self, request):
        field_name = request.POST.get("__field_name__")
        form = self.form_class(request.POST)
        form.is_valid()
        errors = form.errors.get(field_name, [])
        return JsonResponse({
            "__field_name__": field_name,
            "errors": errors,
        })

class MedicineTypeValidationFormView(View):
    form_class = MedicineTypeForm
    # template_name = "webapp/contact.html"
    # success_url = "/success/"

    def post(self, request, *args, **kwargs):
        if "__field_name__" in request.POST:
            return self.validate_field(request)
        return HttpResponse()

    def validate_field(self, request):
        field_name = request.POST.get("__field_name__")
        form = self.form_class(request.POST)
        form.is_valid()
        errors = form.errors.get(field_name, [])
        return JsonResponse({
            "__field_name__": field_name,
            "errors": errors,
        })

class PatientValidationFormView(View):
    form_class = PatientCreateUpdateForm
    # template_name = "webapp/contact.html"
    # success_url = "/success/"

    def post(self, request, *args, **kwargs):
        if "__field_name__" in request.POST:
            return self.validate_field(request)
        return HttpResponse()

    def validate_field(self, request):
        field_name = request.POST.get("__field_name__")
        form = self.form_class(request.POST)
        form.is_valid()
        errors = form.errors.get(field_name, [])
        return JsonResponse({
            "__field_name__": field_name,
            "errors": errors,
        })