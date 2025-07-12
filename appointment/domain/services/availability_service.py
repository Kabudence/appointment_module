from datetime import datetime

from appointment.infraestructure.repositories.appointment_repository import AppointmentRepository
from schedules.domain.services.schedule_service import find_available_slots
from schedules.infraestructure.repositories.schedule_repository import ScheduleRepository
from staff.infraestructure.repositories.staff_repository import StaffRepository




class AvailabilityService:
    def __init__(self,
                 schedule_repo: ScheduleRepository,
                 staff_repo: StaffRepository,
                 appointment_repo: AppointmentRepository):
        self.schedule_repo = schedule_repo
        self.staff_repo = staff_repo
        self.appointment_repo = appointment_repo

    # 1️⃣ Para la pantalla “lista de horarios disponibles”
    def find_available_slots_for_day(self,
                                     negocio_id: int,
                                     business_id: int,
                                     day: str,
                                     service_duration_min: int) -> list[dict]:
        """
        Devuelve slots [{start_time, end_time}] donde *al menos un* staff está libre.
        """
        # A. Obtén el schedule (08-22) de ese día
        schedule = self.schedule_repo.get_by_day_and_business_and_negocio(
            day,business_id, negocio_id)

        # B. Obtén todos los staff que trabajan en ese negocio/local
        staff_ids = [s.id for s in self.staff_repo.list_by_negocio_business(
            negocio_id, business_id)]

        # C. Agrupa citas por staff
        appointments_by_staff = {
            sid: self.appointment_repo.list_by_staff_and_day(sid, day)
            for sid in staff_ids
        }

        # D. Usa tu función `find_available_slots`, pero por staff.
        #    Luego une los resultados (slot está libre si ≥1 staff libre).
        free_union = set()
        for sid, citas in appointments_by_staff.items():
            occupied = [
                {"start_time": a.start_time.strftime("%H:%M"),
                 "end_time":   a.end_time.strftime("%H:%M")}
                for a in citas
            ]
            staff_free = find_available_slots(schedule,
                                              service_duration_min,
                                              occupied)
            for slot in staff_free:
                free_union.add((slot["start_time"], slot["end_time"]))

        # Convertir a lista ordenada
        return [
            {"start_time": s, "end_time": e}
            for s, e in sorted(free_union)
        ]

    # 2️⃣ Al momento de “Confirmar” la cita
    def pick_first_free_staff(self,
                              negocio_id: int,
                              business_id: int,
                              start: datetime,
                              end: datetime) -> int | None:
        """Devuelve un staff_id libre, o None si todos ocupados."""
        staff_ids = [s.id for s in self.staff_repo.list_by_negocio_business(
            negocio_id, business_id)]
        for sid in staff_ids:
            if self.appointment_repo.is_staff_free(sid, start, end):
                return sid
        return None
