from typing import Optional, Dict, Any

from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.db.models import Q
from account.models import User
from account.mixins import RoleRequiredMixin
from base.views import LoginRequiredView

from clinic_management.models import Patient
from clinic_management.forms.patient_forms import PatientCreateUpdateForm


class PatientCreateView(LoginRequiredView, RoleRequiredMixin, CreateView):
    roles_required = [ User.UserRole.ASSISTANT ]
    model = Patient
    template_name: str = 'patient/patient_form.html'
    form_class = PatientCreateUpdateForm
    context_object_name: Optional[str] = 'form'
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        return super().get_context_data(**kwargs)

    def get_success_url(self) -> str:
        messages.success(request=self.request, message='Create patient successfully')
        return reverse('clinic_management:patient_index')

class PatientEditView(LoginRequiredView, RoleRequiredMixin, UpdateView):
    roles_required = [ User.UserRole.ASSISTANT ]
    model = Patient
    template_name: str = 'patient/patient_form.html'
    form_class = PatientCreateUpdateForm
    context_object_name: Optional[str] = 'form'
    def get_success_url(self) -> str:
        messages.success(request=self.request, message="Edit patient successfully")
        return reverse('clinic_management:patient_index')
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['action'] = 'edit'
        context['pk'] = self.kwargs.get('pk')
        return context



class PatientListView(LoginRequiredView, RoleRequiredMixin, ListView):
    roles_required = [ User.UserRole.BASE ]
    model = Patient
    template_name = 'patient/index.html'
    context_object_name: Optional[str] = 'patients'
    paginate_by: int = 10
    def get_queryset(self):
        keyword = self.request.GET.get('q','')
        queryset = super().get_queryset()
        return queryset.filter(
            Q(name__contains=keyword) | Q(address__contains=keyword) | Q(phone__contains=keyword)
        ).order_by('-created_at')

class PatientDetailView(RoleRequiredMixin, DetailView):
    roles_required = [ User.UserRole.BASE ]
    model = Patient
    template_name: str = 'patient/detail.html'
    context_object_name: Optional[str] = 'patient'


class PatientDeleteView(LoginRequiredView, RoleRequiredMixin ,DeleteView):
    roles_required = [ User.UserRole.ASSISTANT ]
    model = Patient
    success_url: Optional[str] = reverse_lazy('clinic_management:patient_index')
    def get_success_url(self) -> str:
        messages.success(self.request, 'Delete successfully')
        return reverse('clinic_management:patient_index')
    def delete(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.soft_delete()
        return HttpResponseRedirect(success_url)
