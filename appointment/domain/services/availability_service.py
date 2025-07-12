from datetime import datetime

from appointment.infraestructure.repositories.appointment_repository import AppointmentRepository
from schedules.domain.services.schedule_service import find_available_slots
from schedules.infraestructure.repositories.schedule_repository import ScheduleRepository
from schedules.infraestructure.repositories.schedule_staff_repository import ScheduleStaffRepository
from staff.infraestructure.repositories.staff_repository import StaffRepository

class AvailabilityService:
    def __init__(
        self,
        schedule_repo: ScheduleRepository,
        schedule_staff_repo: ScheduleStaffRepository,
        staff_repo: StaffRepository,
        appointment_repo: AppointmentRepository
    ):
        self.schedule_repo = schedule_repo
        self.schedule_staff_repo = schedule_staff_repo
        self.staff_repo = staff_repo
        self.appointment_repo = appointment_repo

    def find_available_slots_for_day(
        self,
        negocio_id: int,
        business_id: int,
        day: str,
        service_duration_min: int
    ) -> list[dict]:
        """
        Devuelve slots [{start_time, end_time}] donde *al menos un* staff asignado a ese horario está libre.
        """
        # 1. Obtén el schedule del día
        schedule = self.schedule_repo.get_by_day_and_business_and_negocio(
            day, business_id, negocio_id
        )
        if not schedule:
            return []

        # 2. Obtén los staff_ids asignados a ese horario
        staff_ids = self.schedule_staff_repo.get_staff_ids_by_schedule(schedule.id)
        if not staff_ids:
            return []

        # 3. Agrupa citas por staff
        appointments_by_staff = {
            sid: self.appointment_repo.list_by_staff_and_day(sid, day)
            for sid in staff_ids
        }

        # 4. Para cada staff, calcula sus slots libres
        free_union = set()
        for sid, citas in appointments_by_staff.items():
            occupied = [
                {"start_time": a.start_time.strftime("%H:%M"),
                 "end_time": a.end_time.strftime("%H:%M")}
                for a in citas
            ]
            staff_free = find_available_slots(schedule, service_duration_min, occupied)
            for slot in staff_free:
                free_union.add((slot["start_time"], slot["end_time"]))

        # 5. Devuelve slots ordenados
        return [
            {"start_time": s, "end_time": e}
            for s, e in sorted(free_union)
        ]

    def pick_first_free_staff(
        self,
        negocio_id: int,
        business_id: int,
        day: str,
        start: datetime,
        end: datetime
    ) -> int | None:
        """
        Devuelve un staff_id asignado al schedule del día que esté libre, o None si todos ocupados.
        """
        schedule = self.schedule_repo.get_by_day_and_business_and_negocio(
            day, business_id, negocio_id
        )
        if not schedule:
            return None
        staff_ids = self.schedule_staff_repo.get_staff_ids_by_schedule(schedule.id)
        for sid in staff_ids:
            if self.appointment_repo.is_staff_free(sid, start, end):
                return sid
        return None
