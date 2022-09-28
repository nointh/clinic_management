from django.contrib import admin
from invoice.models import Invoice, InvoiceDetail

# Register your models here.

class CustomInvoiceAdmin(admin.ModelAdmin):
    pass

admin.site.register(Invoice, CustomInvoiceAdmin)
admin.site.register(InvoiceDetail)
