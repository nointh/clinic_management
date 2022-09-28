from typing import Any, Dict, Optional
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django.views import View
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from django.template.loader import render_to_string,get_template
from django.template import engines
from django.conf import settings

import io
from django.http import FileResponse

from xhtml2pdf import pisa

from prescription.forms import PrescriptionCreateForm
from prescription.models import Prescription
from prescription.services import PrescriptionService

# Create your views here.
class PrescriptionListView(ListView):
    template_name: str = 'prescription/index.html'
    model = Prescription
    paginate_by: int = 10
    # context_object_name: Optional[str] = 'prescription_list'
    def get_queryset(self, **kwargs: Any) -> Dict[str, Any]:
        query = self.request.GET.get('q', '')
        
        object_list = Prescription.objects.filter(
            Q(diagnosis__contains=query) | Q(patient__name__contains=query)
        ).order_by('-modified_at')
        return object_list


# class PrescriptionDetailView(DetailView):
#     model = Prescription
#     template_name: str = 'prescription/detail.html'
#     context_object_name: Optional[str] = 'prescription'

#     def get_queryset(self):
#         return super().get_queryset().filter(id=self.kwargs['pk'])
    
#     def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
#         return super().get_context_data(**kwargs)

class PrescriptionDetailView(View):
    model = Prescription

    def get(self, request, pk):
        prescription = Prescription.objects.get(pk=pk)
        context = {
            'prescription': prescription
        }
        return render(request, 'prescription/detail.html', context)

    def post(self, request, pk):
        prescription = Prescription.objects.get(pk=pk)
        form = PrescriptionCreateForm(request.POST, instance=prescription)
        print(request.POST)
        medicine_ids =  request.POST.getlist('medicine-ids')
        medicine_numbers = request.POST.getlist('medicine-numbers')
        medicine_usages = request.POST.getlist('medicine-usages')
        print(medicine_ids)
        print(medicine_numbers)
        print(medicine_usages)
        service = PrescriptionService()
        if service.edit_prescription_and_detail(form, medicine_ids=medicine_ids, medicine_numbers=medicine_numbers, medicine_usages=medicine_usages):

            messages.success(request=request, message='Edit prescription successfully')
            return redirect('prescription:index')
        else:
            return render(request, 'prescription/prescription_form.html', context={'form': form })

    def delete(self, request, pk):
        prescription = get_object_or_404(Prescription, pk=pk)
        prescription.delete()
        messages.success(request=request, message='Delete prescription successfully')
        return redirect('prescription:index')




class PrescriptionCreateView(View):
    model = Prescription
    def get(self, request):
        form = PrescriptionCreateForm()
        return render(request, 'prescription/prescription_form.html', {'form': form }) 

    def post(self, request):
        form = PrescriptionCreateForm(request.POST)
        print(request.POST)
        medicine_ids = [i for i in request.POST.getlist('medicine-ids')]
        medicine_numbers = [i for i in request.POST.getlist('medicine-numbers')]
        medicine_usages = [i for i in request.POST.getlist('medicine-usages')]
        print(medicine_ids)
        print(medicine_numbers)
        print(medicine_usages)
        service = PrescriptionService()
        if service.create_prescription_and_detail(form, medicine_ids=medicine_ids, medicine_numbers=medicine_numbers, medicine_usages=medicine_usages):

            messages.success(request=request, message='Create prescription successfully')
            return redirect('prescription:index')
        else:
            return render(request, 'prescription/prescription_form.html', context={'form': form })

class PrescriptionEditView(View):
    model = Prescription
    def get(self, request, pk):
        prescription = Prescription.objects.get(pk=pk)
        form = PrescriptionCreateForm(instance=prescription)
        context = {
            'form': form,
            'details': prescription.prescriptiondetail_set.all(),
            'action': 'edit',
            'pk': pk
        }
        return render(request, 'prescription/prescription_form.html', context=context)
    def post(self, request, pk):
        prescription = Prescription.objects.get(pk=pk)
        form = PrescriptionCreateForm(request.POST, instance=prescription)
        print(request.POST)
        medicine_ids =  request.POST.getlist('medicine-ids')
        medicine_numbers = request.POST.getlist('medicine-numbers')
        medicine_usages = request.POST.getlist('medicine-usages')
        print(medicine_ids)
        print(medicine_numbers)
        print(medicine_usages)
        service = PrescriptionService()
        if service.edit_prescription_and_detail(form, medicine_ids=medicine_ids, medicine_numbers=medicine_numbers, medicine_usages=medicine_usages):

            messages.success(request=request, message='Edit prescription successfully')
            return redirect('prescription:index')
        else:
            messages.error(request=request, message='Failed to edit prescription')
            return render(request, 'prescription/prescription_form.html', context={'form': form })

class PrescriptionDeleteView( DeleteView):
    model = Prescription
    success_url: Optional[str] = reverse_lazy('prescription:index')
    def get_success_url(self) -> str:
        messages.success(self.request, 'Delete successfully')
        return reverse('prescription:index')

    def form_valid(self, form):
        success_url = self.get_success_url()
        print('here im soft delete in form valid')
        print(self.object)
        self.object.soft_delete()
        return HttpResponseRedirect(success_url)





class PrescriptionPdfView(View):

    def get(self, request, pk) -> Dict[str, Any]:
        prescription = Prescription.objects.get(pk=pk)
        context = { 'prescription': prescription}
        template = get_template('pdf/prescription_pdf.html')
        html  = template.render(context)
        result = io.BytesIO()
        pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        return None
    
class PdfView(View):
    def get(self, request, pk) -> Dict[str, Any]:
        prescription = Prescription.objects.get(pk=pk)
        context = { 'prescription': prescription}
        template = get_template('pdf/prescription_pdf.html')
        html  = template.render(context)
        result = io.BytesIO()
        pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
        if not pdf.err:
            return HttpResponse(html)
        return None

