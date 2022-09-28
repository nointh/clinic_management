from .models import Medicine
from django import forms
class MedicineCreateForm(forms.ModelForm):
    class Meta:
        model = Medicine
        exclude = ('deleted_at',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['medicine_type'].widget.attrs['class'] = 'form-select'
