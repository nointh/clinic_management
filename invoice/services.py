from invoice.forms import InvoiceCreateOrEditForm
from invoice.models import Invoice, InvoiceDetail
from medicine.models import Medicine

def is_float(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
class InvoiceService:
    def __init__(self) -> None:
        pass

    
    def is_invoice_detail_valid(self, medicine_ids, medicine_quanties, medicine_prices) -> bool:
        return len(medicine_ids) == len(medicine_quanties)\
            and len(medicine_quanties) == len(medicine_prices) \
            and all(num.isdigit() for num in medicine_quanties) \
            and all(is_float(num) for num in medicine_prices)

    def create_invoice_and_detail(self, form: InvoiceCreateOrEditForm | Invoice, medicine_ids, medicine_quantities, medicine_prices):
        if form.is_valid() and self.is_invoice_detail_valid(medicine_ids, medicine_quantities, medicine_prices):
            invoice = form.save()
            total = 0
            for i in range(len(medicine_ids)):
                total += int(medicine_quantities[i]) * int(medicine_prices[i])
                invoice_detail = InvoiceDetail(medicine=Medicine.objects.get(pk=medicine_ids[i]),\
                    invoice=invoice,\
                    quantity=int(medicine_quantities[i]),\
                    unit_price=float(medicine_prices[i]))
                invoice_detail.save()
            print('totalllzlzl: ' + str(invoice.get_total))
            invoice.total = invoice.get_total
            invoice.save()
            return True
        return False
    
    def edit_invoice_and_detail(self, form: InvoiceCreateOrEditForm | Invoice, medicine_ids, medicine_quantities, medicine_prices):
        if form.is_valid() and self.is_invoice_detail_valid(medicine_ids, medicine_quantities, medicine_prices):
            print(medicine_quantities)
            print(medicine_prices)
            invoice = form.save()
            invoice_details = invoice.invoicedetail_set.all()
            new_medicine_id_set = {id for id in medicine_ids}
            old_medicine_id_set = {str(detail.medicine.id) for detail in invoice_details}
            print('new === ')
            print(new_medicine_id_set)

            print('old === ')
            print(old_medicine_id_set)


            print('update =========' )
            print(new_medicine_id_set & old_medicine_id_set)
            print('create =========' )
            print(new_medicine_id_set - old_medicine_id_set)

            print('delete =========' )
            print(old_medicine_id_set - new_medicine_id_set)

            for i in range(len(medicine_ids)):
                #update => new medicine with id have already in old set
                if medicine_ids[i] in new_medicine_id_set & old_medicine_id_set:
                    print('edit new detail medicine id  = '+medicine_ids[i])

                    detail = invoice_details.get(medicine__id=medicine_ids[i])
                    detail.quantity = int(medicine_quantities[i])
                    detail.unit_price = float(medicine_prices[i])
                    detail.save()
                #create => new medicine with id don't have in old set
                elif medicine_ids[i] in new_medicine_id_set - old_medicine_id_set:
                    print('create new detail medicine id  = '+medicine_ids[i])
                    detail = InvoiceDetail(medicine=Medicine.objects.get(pk=medicine_ids[i]),\
                        invoice=invoice,\
                        quantity= int(medicine_quantities[i]),\
                        unit_price= float(medicine_prices[i]))
                    detail.save()
            #delete => old medicine with id don't have in new id set
            for id in old_medicine_id_set - new_medicine_id_set:
                print('delete new detail medicine id  = '+id)

                detail = invoice_details.get(medicine__id=id)
                detail.delete()

            print('totalllzlzl update: ' + str(invoice.get_total))
            invoice.total = invoice.get_total

            invoice.save()
            return True
        return False
            
            