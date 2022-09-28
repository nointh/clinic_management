from django.contrib import admin
from .models import Prescription, PrescriptionDetail
# Register your models here.
admin.site.register(Prescription)
admin.site.register(PrescriptionDetail)