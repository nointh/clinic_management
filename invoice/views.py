from django.shortcuts import render
from django.views import View
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from typing import List, Any, Dict, Optional

from invoice.models import Invoice
from invoice.forms import InvoiceCreateOrEditForm
from invoice.services import InvoiceService
# Create your views here.


class InvoiceListView(ListView):
    template_name: str = 'invoice/index.html'
    model = Invoice
    paginate_by: int = 10
    # context_object_name: Optional[str] = 'invoice_list'
    def get_queryset(self, **kwargs: Any) -> Dict[str, Any]:
        query = self.request.GET.get('q', '')
        
        object_list = Invoice.objects.filter(patient__name__contains=query).order_by('-modified_at')
        return object_list


# class InvoiceDetailView(DetailView):
#     model = Invoice
#     template_name: str = 'invoice/detail.html'
#     context_object_name: Optional[str] = 'invoice'

#     def get_queryset(self):
#         return super().get_queryset().filter(id=self.kwargs['pk'])
    
#     def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
#         return super().get_context_data(**kwargs)

class InvoiceDetailView(View):
    model = Invoice

    def get(self, request, pk):
        invoice = Invoice.objects.get(pk=pk)
        context = {
            'invoice': invoice
        }
        return render(request, 'invoice/detail.html', context)

    def post(self, request, pk):
        invoice = Invoice.objects.get(pk=pk)
        form = InvoiceCreateOrEditForm(request.POST, instance=invoice)
        print(request.POST)
        medicine_ids =  request.POST.getlist('medicine-ids')
        medicine_quantities = request.POST.getlist('medicine-quantities')
        medicine_prices = request.POST.getlist('medicine-unit-prices')
        print(medicine_ids)
        print(medicine_quantities)
        print(medicine_prices)
        service = InvoiceService()
        if service.edit_invoice_and_detail(form, medicine_ids=medicine_ids, medicine_quantities=medicine_quantities, medicine_prices=medicine_prices):

            messages.success(request=request, message='Edit invoice successfully')
            return redirect('invoice:index')
        else:
            return render(request, 'invoice/invoice_form.html', context={'form': form })

    def delete(self, request, pk):
        invoice = get_object_or_404(Invoice, pk=pk)
        invoice.delete()
        messages.success(request=request, message='Delete invoice successfully')
        return redirect('invoice:index')




class InvoiceCreateView(View):
    model = Invoice
    def get(self, request):
        form = InvoiceCreateOrEditForm()
        return render(request, 'invoice/invoice_form.html', {'form': form }) 

    def post(self, request):
        form = InvoiceCreateOrEditForm(request.POST)
        print(request.POST)
        medicine_ids = [i for i in request.POST.getlist('medicine-ids')]
        medicine_quantities = [i for i in request.POST.getlist('medicine-quantities')]
        medicine_prices = [i for i in request.POST.getlist('medicine-unit-prices')]
        print(medicine_ids)
        print(medicine_quantities)
        print(medicine_prices)
        service = InvoiceService()
        if service.create_invoice_and_detail(form, medicine_ids=medicine_ids, \
            medicine_quantities=medicine_quantities, medicine_prices=medicine_prices):

            messages.success(request=request, message='Create invoice successfully')
            return redirect('invoice:index')
        else:
            return render(request, 'invoice/invoice_form.html', context={'form': form })

class InvoiceEditView(View):
    model = Invoice
    def get(self, request, pk):
        invoice = Invoice.objects.get(pk=pk)
        form = InvoiceCreateOrEditForm(instance=invoice)
        context = {
            'form': form,
            'details': invoice.invoicedetail_set.all(),
            'action': 'edit',
            'pk': pk
        }
        return render(request, 'invoice/invoice_form.html', context=context)
    def post(self, request, pk):
        invoice = Invoice.objects.get(pk=pk)
        form = InvoiceCreateOrEditForm(request.POST, instance=invoice)
        print(request.POST)
        medicine_ids =  request.POST.getlist('medicine-ids')
        medicine_quantities = request.POST.getlist('medicine-quantities')
        medicine_prices = request.POST.getlist('medicine-unit-prices')
        print(medicine_ids)
        print(medicine_quantities)
        print(medicine_prices)
        service = InvoiceService()
        if service.edit_invoice_and_detail(form, medicine_ids=medicine_ids, medicine_quantities=medicine_quantities, medicine_prices=medicine_prices):

            messages.success(request=request, message='Edit invoice successfully')
            return redirect('invoice:index')
        else:
            messages.error(request=request, message='Failed to edit invoice')
            context = {
                'form': form,
                'details': invoice.invoicedetail_set.all(),
                'action': 'edit',
                'pk': pk
            }
            return render(request, 'invoice/invoice_form.html', context=context)

            # return render(request, 'invoice/invoice_form.html', context={'form': form })

class InvoiceDeleteView( DeleteView):
    model = Invoice
    success_url: Optional[str] = reverse_lazy('invoice:index')
    def get_success_url(self) -> str:
        messages.success(self.request, 'Delete successfully')
        return reverse('invoice:index')