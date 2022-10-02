from clinic_management.models import Patient
from django import forms
class PatientCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ('created_date', 'deleted_at')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        # self.fields['gender'].widget.attrs['class'] = 'form-select'
