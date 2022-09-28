from patient.forms import PatientCreateUpdateForm
from patient.models import Patient


class PatientService:
    @staticmethod
    def create_patient(patient: PatientCreateUpdateForm | Patient):
        
        result = patient.save()
        message = { 'text': '', 'status': ''}
        if result != None:
            message = { 'text': "Create new patient successfully", 'status': 'success'}
        else: 
            message = { 'text': "Fail to create new patient", 'status': 'failed'}
        return message
    
