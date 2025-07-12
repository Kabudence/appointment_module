from datetime import datetime

from appointment.domain.entities.appointment import Appointment, AppointmentStatus
from appointment.infraestructure.repositories.appointment_repository import AppointmentRepository

class AppointmentCommandService:
    def __init__(self, appointment_repo: AppointmentRepository):
        self.appointment_repo = appointment_repo

    def create(
            self,
            start_time: datetime,
            end_time: datetime,
            client_id: int,
            negocio_id: int,
            staff_id: int,
            business_id: int,
            service_id: int,
            status: str = AppointmentStatus.PENDING.value,
    ) -> Appointment:
        # 1. Validación de campos básicos
        if not (start_time and end_time and client_id and staff_id and business_id and service_id):
            raise ValueError("Missing required fields.")
        if start_time >= end_time:
            raise ValueError("End time must be after start time.")

        # 2. Verifica que el staff esté libre en ese horario
        if not self.appointment_repo.is_staff_free(staff_id, start_time, end_time):
            raise ValueError("Staff not available for the selected time.")

        # 3. (Opcional) Verifica que el horario y staff pertenezcan al schedule del día
        # schedule = self.schedule_repo.get_by_day_and_business_and_negocio(day, business_id, negocio_id)
        # staff_ids = self.schedule_staff_repo.get_staff_ids_by_schedule(schedule.id)
        # if staff_id not in staff_ids:
        #     raise ValueError("Staff is not assigned to the selected schedule.")

        # 4. Crea la cita
        appt = Appointment(
            start_time=start_time,
            end_time=end_time,
            client_id=client_id,
            negocio_id=negocio_id,
            staff_id=staff_id,
            business_id=business_id,
            service_id=service_id,
        )
        return self.appointment_repo.create(appt)

    def update_status(self, appointment_id: int, new_status: str) -> Appointment:
        # Actualiza solo el estado
        appt = self.appointment_repo.get_by_id(appointment_id)
        if not appt:
            raise ValueError("Appointment not found")
        appt.status = new_status
        return self.appointment_repo.update(appt)

    def cancel(self, appointment_id: int) -> Appointment:
        # Un wrapper para marcar como cancelado
        return self.update_status(appointment_id, AppointmentStatus.CANCELLED.value)
