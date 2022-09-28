from typing import Iterable, Optional
from datetime import datetime
from django.db import models

from medicine.models import Medicine
from patient.models import Patient
from base.models import SoftDeleteAbstractModel
# Create your models here.
class Invoice(SoftDeleteAbstractModel):
    id = models.BigAutoField(primary_key=True, editable=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    medicines = models.ManyToManyField(to=Medicine, through='InvoiceDetail', through_fields=['invoice', 'medicine'])
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
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

    # def save(self, *args, **kwargs) -> None:
    #     self.total = self.get_total
    #     return super(Invoice, self).save(*args, **kwargs)

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