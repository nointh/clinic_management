from django.db import models
import datetime
from base.models import SoftDeleteAbstractModel
from account.models import User
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
    
    def __str__(self) -> str:
        return self.name


class MedicineType(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.name

    
class Medicine(SoftDeleteAbstractModel):
    id = models.BigAutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=200)
    stock_quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=30)
    usage = models.CharField(max_length=100, blank=True)
    origin_price = models.FloatField()
    sale_price = models.FloatField()
    dose_per_day = models.FloatField()
    medicine_type = models.ForeignKey(MedicineType, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.name


class Prescription(SoftDeleteAbstractModel):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    diagnosis = models.CharField(max_length=300)
    note = models.CharField(max_length=300, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
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


class Invoice(SoftDeleteAbstractModel):
    id = models.BigAutoField(primary_key=True, editable=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    medicines = models.ManyToManyField(to=Medicine, through='InvoiceDetail', through_fields=['invoice', 'medicine'])
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField(default=0)

    def __str__(self) -> str:
        return 'invoice - ' + str(self.id)
    
    def soft_delete(self):
        self.invoicedetail_set.all().update(deleted_at=datetime.now())
        return SoftDeleteAbstractModel.soft_delete()
    
    def restore(self):
        self.invoicedetail_set.all().update(deleted_at=None)
        return SoftDeleteAbstractModel.restore()
    
    @property
    def get_total(self):
        # invoice = Invoice.objects.get(pk=self.id)
        query_result = self.invoicedetail_set.all().aggregate(total_price = models.Sum('line_total'))
        return query_result['total_price']


class InvoiceDetail(SoftDeleteAbstractModel):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    unit_price = models.FloatField(default=0)
    line_total = models.FloatField(default=0)
    @property
    def get_line_total(self):
        return self.quantity * self.unit_price\

    def save(self, *args, **kwargs) -> None:
        self.line_total = self.get_line_total
        return super(InvoiceDetail, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'invoice detail I{self.invoice.id} - M{self.medicine.id}'
    
    class Meta:
        unique_together = (('invoice', 'medicine'),)