from datetime import datetime, time
from appointment.infraestructure.repositories.appointment_repository import AppointmentRepository
from schedules.domain.entities.schedule import Schedule
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
        appointment_repo: AppointmentRepository,
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
        service_duration_min: int,
    ) -> list[dict]:

        print(f"\n[AVAIL] ▶️  Buscando slots — negocio={negocio_id} "
              f"business={business_id} day={day} dur={service_duration_min}")

        # 0. Trae el schedule (único) del día
        schedule = self.schedule_repo.get_by_day_and_business_and_negocio(
            day, business_id, negocio_id
        )
        if not schedule:
            print("[AVAIL] ⚠️  No existe schedule para esos parámetros")
            return []

        print(f"[AVAIL]    Schedule encontrado id={schedule.id} "
              f"{schedule.start_time}-{schedule.end_time}")

        # 1. Normaliza horas a "HH:MM"
        def _to_hhmm(h): return h.strftime("%H:%M") if isinstance(h, time) else str(h)

        schedule_for_calc = Schedule(
            id=schedule.id,
            day=schedule.day,
            start_time=_to_hhmm(schedule.start_time),
            end_time=_to_hhmm(schedule.end_time),
            negocio_id=schedule.negocio_id,
            business_id=schedule.business_id,
            is_active=schedule.is_active,
        )

        # 2. Staff asignado
        staff_ids = self.schedule_staff_repo.get_staff_ids_by_schedule(schedule.id)
        print(f"[AVAIL]    Staff asignado al schedule: {staff_ids}")
        if not staff_ids:
            print("[AVAIL] ⚠️  El schedule no tiene staff asociado")
            return []

        # 3. Para cada staff: citas ocupadas y slots libres
        free_union: set[tuple[str, str]] = set()

        for sid in staff_ids:
            citas = self.appointment_repo.list_by_staff_and_day(sid, day)
            print(f"[AVAIL]      • Staff {sid} tiene {len(citas)} cita(s) ese día")

            occupied = [
                {
                    "start_time": a.start_time.strftime("%H:%M"),
                    "end_time": a.end_time.strftime("%H:%M"),
                }
                for a in citas
            ]
            if occupied:
                print(f"[AVAIL]        Ocupadas → {occupied}")

            staff_free = find_available_slots(
                schedule_for_calc, service_duration_min, occupied
            )
            print(f"[AVAIL]        Libres   → {staff_free}")

            for slot in staff_free:
                free_union.add((slot["start_time"], slot["end_time"]))

        # 4. Resultado final
        result = [
            {"start_time": s, "end_time": e}
            for s, e in sorted(free_union)
        ]
        print(f"[AVAIL] ✅ Slots finales (unión) → {result}\n")
        return result


    def pick_first_free_staff(
        self,
        negocio_id: int,
        business_id: int,
        day: str,
        start: datetime,
        end: datetime,
    ) -> int | None:

        print(f"\n[AVAIL] ▶️  Buscando staff libre — "
              f"day={day} {start.strftime('%H:%M')}-{end.strftime('%H:%M')}")

        schedule = self.schedule_repo.get_by_day_and_business_and_negocio(
            day, business_id, negocio_id
        )
        if not schedule:
            print("[AVAIL] ⚠️  Sin schedule para ese día")
            return None

        staff_ids = self.schedule_staff_repo.get_staff_ids_by_schedule(schedule.id)
        print(f"[AVAIL]    Staff en el schedule: {staff_ids}")

        for sid in staff_ids:
            libre = self.appointment_repo.is_staff_free(sid, start, end)
            print(f"[AVAIL]      • Staff {sid} libre? {libre}")
            if libre:
                print(f"[AVAIL] ✅  Primer staff libre → {sid}\n")
                return sid

        print("[AVAIL] ❌  Todos ocupados\n")
        return None
