from django.db import models
from medicine.models import Medicine
from patient.models import Patient
from base.models import SoftDeleteAbstractModel
# Create your models here.
class Prescription(SoftDeleteAbstractModel):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    diagnosis = models.CharField(max_length=300)
    note = models.CharField(max_length=300, blank=True, null=True)
    # medicines = models.ManyToManyField(Medicine)
    medicines = models.ManyToManyField(Medicine, through="PrescriptionDetail", through_fields=['prescription','medicine'])
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return f"{str(self.patient)} {self.diagnosis} {self.created_at.strftime('%d/%m/%Y')}"


class PrescriptionDetail(SoftDeleteAbstractModel):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    usage = models.CharField(max_length=100)
    number = models.IntegerField(default=0)
    class Meta:
        unique_together = (("prescription", "medicine"),)
