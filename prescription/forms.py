from django.forms import ModelForm
from django import forms

from prescription.models import Prescription

class PrescriptionCreateForm(ModelForm):
    class Meta:
        model = Prescription
        exclude = ('created_at', 'medicines', 'deleted_at')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
