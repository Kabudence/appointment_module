from datetime import datetime

from peewee import fn

from appointment.domain.entities.appointment import Appointment, AppointmentStatus
from appointment.infraestructure.models.appointment_model import AppointmentModel


class AppointmentRepository:
    def get_by_day_negocio_id(self, day: str, negocio_id: int) -> list:
        """
        Retrieves appointments for a specific day (YYYY-MM-DD) and negocio_id.
        """
        query = AppointmentModel.select().where(
            (fn.DATE(AppointmentModel.start_time) == day) &
            (AppointmentModel.negocio_id == negocio_id)
        )
        return [self._from_model(record) for record in query]

    def list_by_staff_and_day(self, staff_id: int, day: str):
        """Todas las citas de un staff en una fecha (YYYY-MM-DD)."""
        return (AppointmentModel
                .select()
                .where(
                    (fn.DATE(AppointmentModel.start_time) == day) &
                    (AppointmentModel.staff_id == staff_id) &
                    (AppointmentModel.status != AppointmentStatus.CANCELLED.value)
                ))

    def is_staff_free(self,
                      staff_id: int,
                      start: datetime,
                      end: datetime) -> bool:
        """True si el staff no tiene ninguna cita que se superponga."""
        clash = (AppointmentModel
                 .select()
                 .where(
                     (AppointmentModel.staff_id == staff_id) &
                     (AppointmentModel.start_time < end) &
                     (AppointmentModel.end_time   > start) &   # intervalo abierto
                     (AppointmentModel.status != AppointmentStatus.CANCELLED.value)
                 )
                 .exists())
        return not clash





    def _from_model(self, record) -> Appointment:
        # Convierte un AppointmentModel en Appointment
        return Appointment(
            id=record.id,
            start_time=record.start_time,
            end_time=record.end_time,
            client_id=record.client_id,
            negocio_id=record.negocio_id,
            staff_id=record.staff_id,
            status=AppointmentStatus(record.status),
            business_id=record.business_id,
            service_id=record.service_id,
        )