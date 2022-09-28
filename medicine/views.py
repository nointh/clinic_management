from typing import Any, Dict, Optional, Type
from django.shortcuts import render

from medicine.forms import MedicineCreateForm
from .models import Medicine
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy, reverse
from django.http import HttpRequest, HttpResponse
from django.contrib import messages

# Create your views here.
class MedicineListView(ListView):
    model = Medicine
    template_name: str = 'medicine/index.html'
    context_object_name: Optional[str] = 'medicine_list'
    paginate_by: int = 10
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['medicines'] = Medicine.objects.all()
    #     return context
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        object_list = Medicine.objects.filter(
            name__contains=query,
            medicine_type__name__contains=query
        )
        return object_list

class MedicineDeleteView(DeleteView):
    model = Medicine
    success_url: Optional[str] = reverse_lazy('medicine:index')
    def get_success_url(self) -> str:
        messages.success(self.request, 'Delete successfully')
        return reverse('medicine:index')

class MedicineDetailView(DetailView):
    model = Medicine
    template_name: str = 'medicine/detail.html'
    context_object_name: Optional[str] = 'medicine'

class MedicineEditView(UpdateView):
    model = Medicine
    template_name: str = 'medicine/medicine_form.html'
    form_class = MedicineCreateForm
    context_object_name: Optional[str] = 'form'
    success_url: Optional[str] = reverse_lazy('medicine:index')
    def get_success_url(self) -> str:
        messages.success(request=self.request, message='Update successfully')
        return reverse('medicine:index')
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['action'] = 'edit'
        context['pk'] = self.kwargs.get('pk')
        return context

class MedicineCreateView(CreateView):
    model = Medicine
    template_name: str = 'medicine/medicine_form.html'
    form_class = MedicineCreateForm
    context_object_name: Optional[str] = 'form'
    success_url: Optional[str] = reverse_lazy('medicine:index')
    def get_success_url(self) -> str:
        messages.success(request=self.request, message="Create new medicine successfully")
        return reverse('medicine:index')

    