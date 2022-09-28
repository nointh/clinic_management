from datetime import datetime
from uuid import  uuid4
from django.db import models
from medicine.models import Medicine
from base.models import SoftDeleteAbstractModel

# Create your models here.
class Patient(SoftDeleteAbstractModel):
    class Gender(models.TextChoices):
        MALE = 'male'
        FEMALE = 'female'
        UNKNOWN = 'unknown'
    id = models.BigAutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    phone = models.CharField(max_length=20, blank=True, null=True)    
    gender = models.CharField(max_length=20,
                        choices=Gender.choices,
                        default=Gender.UNKNOWN)
    address = models.CharField(max_length=500, blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    temperature = models.FloatField(default=37, blank=True, null=True)
    blood_pressure = models.FloatField(blank=True, null=True)
    heart_rate = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # prescriptions = models.ManyToOne(Prescription, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self) -> str:
        return self.name


# class Prescription(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     diagnosis = models.CharField(max_length=300)
#     note = models.CharField(max_length=300, blank=True, null=True)
#     # medicines = models.ManyToManyField(Medicine)
#     medicines = models.ManyToManyField(Medicine, through="PrescriptionDetail", through_fields=['prescription','medicine'])
#     patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
#     def __str__(self) -> str:
#         return str(self.patient) + self.diagnosis + self.created_at.strftime('%d/%M/%Y')


# class PrescriptionDetail(models.Model):
#     prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
#     medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
#     usage = models.CharField(max_length=100)
#     number = models.IntegerField(default=0)


