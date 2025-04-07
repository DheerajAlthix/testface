from ..models import HealthRecord
from ..schemas import HealthRecordSchema

class HealthRecordService:
    def list_health_records(self, user, is_staff=False):
        if is_staff:
            records = HealthRecord.objects.all()
        else:
            records = HealthRecord.objects.filter(user=user)
        return [HealthRecordSchema.from_orm(record).dict() for record in records]

    def create_health_record(self, data: dict, user):
        record = HealthRecord.objects.create(
            user=user,
            file=data['file'],
            report_type=data['report_type'],
            sample_collection=data['sample_collection'],
            uploaded_by=data['uploaded_by'],
            checked_by=data['checked_by']
        )
        return {"success": True, "data": HealthRecordSchema.from_orm(record).dict()}