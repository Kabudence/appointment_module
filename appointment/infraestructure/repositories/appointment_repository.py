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
        """
        Recibe `day` en cualquiera de estos formatos:
        • '2025-07-14'  → lo convierte a 'Monday'
        • 'Monday'      → lo usa tal cual
        """
        # ── 1. Normaliza a nombre de día ──────────────────────────────
        try:
            # ¿viene como fecha ISO?
            _date = datetime.strptime(day, "%Y-%m-%d")
            day_name = _date.strftime("%A")  # 'Monday', 'Tuesday', …
        except ValueError:
            # No era fecha → asumimos que ya es 'Monday', etc.
            day_name = day

        # ── 2. Consulta por DAYNAME(start_time) ───────────────────────
        return (
            AppointmentModel
            .select()
            .where(
                (fn.DAYNAME(AppointmentModel.start_time) == day_name) &
                (AppointmentModel.staff_id == staff_id) &
                (AppointmentModel.status != AppointmentStatus.CANCELLED.value)
            )
        )

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

    def create(self, appointment: Appointment) -> Appointment:
        # Crea el registro en la base de datos
        record = AppointmentModel.create(
            start_time=appointment.start_time,
            end_time=appointment.end_time,
            client_id=appointment.client_id,
            negocio_id=appointment.negocio_id,
            staff_id=appointment.staff_id,
            business_id=appointment.business_id,
            service_id=appointment.service_id,
            status=appointment.status.value if isinstance(appointment.status, AppointmentStatus) else appointment.status
        )
        # Devuelve el entity actualizado con el id real
        return self._from_model(record)

    def update(self, appointment: Appointment) -> Appointment:
        # Actualiza el registro existente
        query = AppointmentModel.update(
            start_time=appointment.start_time,
            end_time=appointment.end_time,
            client_id=appointment.client_id,
            negocio_id=appointment.negocio_id,
            staff_id=appointment.staff_id,
            business_id=appointment.business_id,
            service_id=appointment.service_id,
            status=appointment.status.value if isinstance(appointment.status, AppointmentStatus) else appointment.status
        ).where(AppointmentModel.id == appointment.id)
        query.execute()
        # Recupera y retorna la versión actualizada
        return self.get_by_id(appointment.id)

    def get_by_id(self, appointment_id: int) -> Appointment | None:
        try:
            record = AppointmentModel.get(AppointmentModel.id == appointment_id)
            return self._from_model(record)
        except AppointmentModel.DoesNotExist:
            return None