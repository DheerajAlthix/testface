from ..models import Appointment
from ..schemas import AppointmentSchema

class AppointmentService:
    def list_appointments(self, user, is_staff=False):
        if is_staff:
            appointments = Appointment.objects.all()
        else:
            appointments = Appointment.objects.filter(patient=user)
        return [AppointmentSchema.from_orm(appointment).dict() for appointment in appointments]

    def create_appointment(self, data: dict, user):
        appointment = Appointment.objects.create(
            patient=user,
            healthcare_provider_id=data['healthcare_provider_id'],
            service_id=data['service_id'],
            appointment_date=data['appointment_date'],
            status=data.get('status', 'scheduled'),
            notes=data.get('notes')
        )
        return {"success": True, "data": AppointmentSchema.from_orm(appointment).dict()}

    def cancel_appointment(self, appointment_id):
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            if appointment.status == 'scheduled':
                appointment.status = 'cancelled'
                appointment.save()
                return {"success": True, "message": "Appointment cancelled"}
            return {"success": False, "message": "Cannot cancel this appointment"}
        except Appointment.DoesNotExist:
            return {"success": False, "message": "Appointment not found"}