from django.db import models
from base.models import SoftDeleteAbstractModel
# Create your models here.
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