from ..models import MedicalHistory
from ..schemas import MedicalHistorySchema

class MedicalHistoryService:
    def list_medical_history(self, user, is_staff=False):
        if is_staff:
            history = MedicalHistory.objects.all()
        else:
            history = MedicalHistory.objects.filter(patient=user)
        return [MedicalHistorySchema.from_orm(entry).dict() for entry in history]

    def create_medical_history(self, data: dict, user):
        history = MedicalHistory.objects.create(
            patient=user,
            condition=data['condition'],
            diagnosis_date=data['diagnosis_date'],
            symptoms=data['symptoms'],
            treatment=data['treatment'],
            medications=data.get('medications'),
            is_ongoing=data['is_ongoing'],
            severity=data['severity'],
            healthcare_provider_id=data['healthcare_provider_id']
        )
        return {"success": True, "data": MedicalHistorySchema.from_orm(history).dict()}