from django.forms import ModelForm
from clinic_management.models import Invoice

class InvoiceCreateOrEditForm(ModelForm):
    class Meta:
        model = Invoice
        exclude = ('created_at','modified_at', 'total', 'medicines', 'deleted_at')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
