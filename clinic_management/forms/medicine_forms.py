from typing import Any, Dict
from django.forms import ValidationError
from clinic_management.models import Medicine
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

    def clean_sale_price(self):
        sale_price = self.cleaned_data['sale_price']
        origin_price = self.cleaned_data['origin_price']
        if sale_price and sale_price < 1000:
            raise forms.ValidationError("We live in VietNam so sale price should me more than 1000")
        if origin_price and origin_price > sale_price:
            raise forms.ValidationError("Sale price must be more than origin price !! This is not charity center")
        return sale_price
    def clean_origin_price(self):
        sale_price = self.cleaned_data['sale_price']
        origin_price = self.cleaned_data['origin_price']
        if  origin_price and origin_price < 1000:
            raise forms.ValidationError("We live in VietNam so sale price should me more than 1000")
        if sale_price and origin_price > sale_price:
            raise forms.ValidationError("Sale price must be more than origin price !! This is not charity center")
        return origin_price
