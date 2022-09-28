from ast import keyword
from contextlib import nullcontext
import json
from typing import Any, Dict, List, Optional
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse, HttpRequest, HttpResponseRedirect
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from patient.services import PatientService
from patient.forms import PatientCreateUpdateForm

from account.mixins import RoleRequiredMixin
from account.models import User
from base.views import LoginRequiredView

from .models import Patient
# Create your views here.
def get_all_patients(request):
    # return HttpResponse("<p>This is the paragraph <h1>big title </h1> </p>")
    patients = Patient.objects.all()
    return render(request, 'patient/index.html', { "patients": patients})

def detail(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    return render(request, 'patient/detail.html', {"patient": patient})
    # return  HttpResponse(f'we are looking for the patient with this id {patient_id}' + f'<h2>{patient.name}</h2>')

def create_patient(request):
    if request.method == 'GET':
        patient_form = PatientCreateUpdateForm()
        return render(request, 'patient/create.html', {'form': patient_form})
    patient_form = PatientCreateUpdateForm(request.POST)
    if patient_form.is_valid():
        result = patient_form.save()
        message = { 'text': '', 'status': ''}
        if result != None:
            message = { 'text': "Create new patient successfully", 'status': 'success'}
        else: 
            message = { 'text': "Fail to create new patient", 'status': 'failed'}

        patients = Patient.objects.all()
        return render(request, 'patient/index.html', { "patients": patients, "message": message})
    
    return render(request, 'patient/create.html', {'form': patient_form})
    
  
def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    patient.delete()
    return HttpResponse('OK')


def test_form(request):
    if request.method == 'GET':
        patient_form = PatientCreateUpdateForm()
        return render(request, 'patient/testform.html', {'form': patient_form})
    elif request.method == 'POST':
        patient_form = PatientCreateUpdateForm(request.POST)
        if patient_form.is_valid():
            message = PatientService.create_patient(patient_form)
            patients = Patient.objects.all()
            messages.success(request=request, message='Create new patient successfully')
            # return render(request, 'patient/index.html', { "patients": patients, "message": message})
            return redirect('patient:index')
        
    return render(request, 'patient/testform.html', {'form': patient_form})

    
    # form = PatientCreateUpdateForm()
    # context = {'form': form, 'action': 'create'}
    # return render(request, 'patient/testform.html', context)

def edit_patient(request, patient_id):
    if request.method == 'GET':
        patient = get_object_or_404(Patient, pk= patient_id)
        form = PatientCreateUpdateForm(instance=patient)
        context = { 'form': form, 'action': 'edit', 'patient_id': patient_id }
        return render(request, 'patient/testform.html', context)
    elif request.method == 'POST':
        patient = get_object_or_404(Patient, pk= patient_id)
        form = PatientCreateUpdateForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            patients = Patient.objects.all()
            return render(request, 'patient/index.html', { "patients": patients, "message": { 'text': "Create new patient successfully", 'status': 'success'}})
        
            
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
        return reverse('patient:index')

class PatientEditView(LoginRequiredView, RoleRequiredMixin, UpdateView):
    roles_required = [ User.UserRole.ASSISTANT ]
    model = Patient
    template_name: str = 'patient/patient_form.html'
    form_class = PatientCreateUpdateForm
    context_object_name: Optional[str] = 'form'
    def get_success_url(self) -> str:
        messages.success(request=self.request, message="Edit patient successfully")
        return reverse('patient:index')
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
        return queryset.filter(name__contains=keyword).order_by('-created_at')

class PatientDetailView(LoginRequiredView, RoleRequiredMixin, DetailView):
    roles_required = [ User.UserRole.BASE ]
    model = Patient
    template_name: str = 'patient/detail.html'
    context_object_name: Optional[str] = 'patient'


class PatientDeleteView(LoginRequiredView, RoleRequiredMixin ,DeleteView):
    roles_required = [ User.UserRole.ASSISTANT ]
    model = Patient
    success_url: Optional[str] = reverse_lazy('patient:index')
    def get_success_url(self) -> str:
        messages.success(self.request, 'Delete successfully')
        return reverse('patient:index')
    def delete(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.soft_delete()
        return HttpResponseRedirect(success_url)
