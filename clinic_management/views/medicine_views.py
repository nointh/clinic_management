from typing import Optional, Dict, Any

from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from account.mixins import RoleRequiredMixin
from account.models import User

from clinic_management.models import Medicine
from clinic_management.forms.medicine_forms import MedicineCreateForm

class MedicineListView(RoleRequiredMixin, ListView):
    roles_required = [ User.UserRole.BASE ]
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
        )\
        .order_by('name')
        return object_list

class MedicineDeleteView(RoleRequiredMixin, DeleteView):
    roles_required = [ User.UserRole.BASE ]

    model = Medicine
    success_url: Optional[str] = reverse_lazy('clinic_management:medicine_index')
    def get_success_url(self) -> str:
        messages.success(self.request, 'Delete successfully')
        return reverse('clinic_management:medicine_index')

class MedicineDetailView(RoleRequiredMixin, DetailView):
    roles_required = [ User.UserRole.BASE ]

    model = Medicine
    template_name: str = 'medicine/detail.html'
    context_object_name: Optional[str] = 'medicine'

class MedicineEditView(RoleRequiredMixin, UpdateView):
    roles_required = [ User.UserRole.BASE ]
    model = Medicine
    template_name: str = 'medicine/medicine_form.html'
    form_class = MedicineCreateForm
    context_object_name: Optional[str] = 'form'
    success_url: Optional[str] = reverse_lazy('clinic_management:medicine_index')
    def get_success_url(self) -> str:
        messages.success(request=self.request, message='Update successfully')
        return reverse('clinic_management:medicine_index')
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['action'] = 'edit'
        context['pk'] = self.kwargs.get('pk')
        return context

class MedicineCreateView(RoleRequiredMixin, CreateView):
    roles_required = [ User.UserRole.BASE ]
    model = Medicine
    template_name: str = 'medicine/medicine_form.html'
    form_class = MedicineCreateForm
    context_object_name: Optional[str] = 'form'
    success_url: Optional[str] = reverse_lazy('clinic_management:medicine_index')
    def get_success_url(self) -> str:
        messages.success(request=self.request, message="Create new medicine successfully")
        return reverse('clinic_management:medicine_index')

    