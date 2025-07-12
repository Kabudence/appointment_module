from datetime import datetime, timedelta

from staff.domain.entities.staff import Staff
from schedules.domain.entities.schedule import Schedule
from appointment.domain.entities.appointment import Appointment, AppointmentStatus

# ---------- Fakes actualizados ----------
class FakeStaffRepo:
    def __init__(self):
        self.staffs = [
            Staff(id=1, speciality="Dentista", name="Ana", negocio_id=1, max_capacity=10, dni="1111"),
            Staff(id=2, speciality="Odontologo", name="Pepe", negocio_id=1, max_capacity=10, dni="2222")
        ]

    def list_by_negocio_business(self, negocio_id, business_id=None):
        print(f"[LOG] list_by_negocio_business(negocio_id={negocio_id})")
        return [s for s in self.staffs if s.negocio_id == negocio_id]

    def get_by_id(self, staff_id):
        for s in self.staffs:
            if s.id == staff_id:
                return s
        return None

class FakeScheduleStaffRepo:
    # Mapea: schedule_id -> [staff_ids]
    def __init__(self):
        self.links = dict()
    def create(self, staff_id, schedule_id):
        if schedule_id not in self.links:
            self.links[schedule_id] = []
        if staff_id in self.links[schedule_id]:
            print(f"[LOG] Relación staff-schedule ya existe: staff={staff_id}, schedule={schedule_id}")
            return False
        print(f"[LOG] Relacionando staff={staff_id} con schedule={schedule_id}")
        self.links[schedule_id].append(staff_id)
        return True
    def get_staff_ids_by_schedule(self, schedule_id):
        return self.links.get(schedule_id, [])

class FakeScheduleRepo:
    def __init__(self):
        self.schedules = []
        self.staff_schedule_repo = None  # se setea después para evitar ciclo
    def create(self, schedule):
        print(f"[LOG] Creando Schedule: {schedule.day} {schedule.start_time}-{schedule.end_time} negocio={schedule.negocio_id}")
        schedule.id = len(self.schedules) + 1
        self.schedules.append(schedule)
        return schedule
    def get_by_negocio_and_businessl(self, negocio_id, business_id=None):
        return [s for s in self.schedules if s.negocio_id == negocio_id]
    def get_by_day_and_business_and_negocio(self, day, business_id, negocio_id):
        # Devuelve el *único* schedule para ese día, negocio y local
        for s in self.schedules:
            if s.day == day and s.negocio_id == negocio_id and (business_id is None or s.business_id == business_id):
                return s
        return None

# Fakes appointments repo
class FakeAppointmentRepo:
    def __init__(self):
        self.appointments = []
    def list_by_staff_and_day(self, staff_id, day):
        return [a for a in self.appointments if a.staff_id == staff_id and a.start_time.strftime("%A") == day]
    def is_staff_free(self, staff_id, start, end):
        for a in self.appointments:
            if a.staff_id == staff_id and not (end <= a.start_time or start >= a.end_time):
                return False
        return True
    def add_appointment(self, appt):
        self.appointments.append(appt)

# Función find_available_slots realista (solo para pruebas)
def find_available_slots(schedule, duration_min, occupied):
    # Crea slots libres dentro del schedule, excepto donde hay ocupadas
    slots = []
    fmt = "%H:%M"
    start = datetime.strptime(schedule.start_time, fmt)
    end = datetime.strptime(schedule.end_time, fmt)
    actual = start
    while (actual + timedelta(minutes=duration_min)) <= end:
        s = actual.strftime(fmt)
        e = (actual + timedelta(minutes=duration_min)).strftime(fmt)
        # Si choca con alguno ocupado, se salta
        overlap = False
        for o in occupied:
            os = datetime.strptime(o["start_time"], fmt)
            oe = datetime.strptime(o["end_time"], fmt)
            if not (actual + timedelta(minutes=duration_min) <= os or actual >= oe):
                overlap = True
                break
        if not overlap:
            slots.append({"start_time": s, "end_time": e})
        actual += timedelta(minutes=duration_min)
    return slots

# ---- Instanciación de todo ----

# 1. Creamos schedule-repo y staff-repo
staff_repo = FakeStaffRepo()
schedule_staff_repo = FakeScheduleStaffRepo()
schedule_repo = FakeScheduleRepo()
schedule_repo.staff_schedule_repo = schedule_staff_repo  # para que schedule pueda saber staff_ids

# 2. ScheduleCommandService corregido para asociar varios staff a un schedule
from schedules.application.commands.schedule_command_service import ScheduleCommandService
class ScheduleCommandServiceV2(ScheduleCommandService):
    def _create_staff_relationships(self, schedule_id, staff_ids):
        if isinstance(staff_ids, int):
            staff_ids = [staff_ids]
        for staff_id in staff_ids:
            self.schedule_staff_repository.create(staff_id, schedule_id)
    # Extra: helper para obtener staff_ids por schedule
    def get_staff_ids_for_schedule(self, schedule_id):
        return self.schedule_staff_repository.get_staff_ids_by_schedule(schedule_id)

schedule_command_service = ScheduleCommandServiceV2(schedule_repo, schedule_staff_repo)

# 3. Creamos un solo schedule lunes, con ambos staff asignados
sch = schedule_command_service.create(
    day="Monday", start_time="08:00", end_time="14:00",
    negocio_id=1, business_id=None, staff_ids=[1, 2]
)

# 4. Fake de citas
appt_repo = FakeAppointmentRepo()
# Ana ya tiene cita de 09:00-10:00
appt_repo.add_appointment(Appointment(
    id=1, start_time=datetime(2024,7,15,9,0), end_time=datetime(2024,7,15,10,0),
    client_id=99, negocio_id=1, staff_id=1, status=AppointmentStatus.PENDING, business_id=None, service_id=1
))

# 5. AvailabilityService que pregunta a ScheduleStaffRepo los staff_ids del schedule
class AvailabilityServiceV2:
    def __init__(self, schedule_repo, schedule_staff_repo, staff_repo, appointment_repo):
        self.schedule_repo = schedule_repo
        self.schedule_staff_repo = schedule_staff_repo
        self.staff_repo = staff_repo
        self.appointment_repo = appointment_repo

    def find_available_slots_for_day(self, negocio_id, business_id, day, service_duration_min):
        schedule = self.schedule_repo.get_by_day_and_business_and_negocio(day, business_id, negocio_id)
        if not schedule:
            print("[ERROR] No hay schedule para ese día/negocio.")
            return []
        staff_ids = self.schedule_staff_repo.get_staff_ids_by_schedule(schedule.id)
        print(f"[LOG] Staff asignados al schedule del lunes: {staff_ids}")

        # Para cada staff, buscamos sus slots libres y hacemos unión
        free_union = set()
        for sid in staff_ids:
            citas = self.appointment_repo.list_by_staff_and_day(sid, day)
            occupied = [
                {"start_time": a.start_time.strftime("%H:%M"),
                 "end_time": a.end_time.strftime("%H:%M")}
                for a in citas
            ]
            staff_free = find_available_slots(schedule, service_duration_min, occupied)
            print(f"[LOG] Staff {sid} ({self.staff_repo.get_by_id(sid).name}) - slots libres: {staff_free}")
            for slot in staff_free:
                free_union.add((slot["start_time"], slot["end_time"]))
        return [{"start_time": s, "end_time": e} for s, e in sorted(free_union)]

    def pick_first_free_staff(self, negocio_id, business_id, start, end):
        schedule = self.schedule_repo.get_by_day_and_business_and_negocio(start.strftime("%A"), business_id, negocio_id)
        if not schedule:
            print("[ERROR] No hay schedule para ese día/negocio.")
            return None
        staff_ids = self.schedule_staff_repo.get_staff_ids_by_schedule(schedule.id)
        for sid in staff_ids:
            if self.appointment_repo.is_staff_free(sid, start, end):
                return sid
        return None

# 6. Probamos el flujo
availability_service = AvailabilityServiceV2(schedule_repo, schedule_staff_repo, staff_repo, appt_repo)

print("\n[LOG] Cliente Pepe entra a reservar cita para Lunes:")

slots = availability_service.find_available_slots_for_day(
    negocio_id=1,
    business_id=None,
    day="Monday",
    service_duration_min=60
)
print(f"[LOG] Horarios disponibles el lunes: {slots}")

slot_elegido = slots[0]
print(f"[LOG] Cliente selecciona slot: {slot_elegido}")

start = datetime.strptime(f"2024-07-15 {slot_elegido['start_time']}", "%Y-%m-%d %H:%M")
end = datetime.strptime(f"2024-07-15 {slot_elegido['end_time']}", "%Y-%m-%d %H:%M")

staff_libre = availability_service.pick_first_free_staff(
    negocio_id=1,
    business_id=None,
    start=start,
    end=end
)
print(f"[LOG] El staff libre para ese horario es: {staff_libre} ({staff_repo.get_by_id(staff_libre).name})")

# Si no le gusta ese staff, prueba el siguiente slot
if len(slots) > 1:
    slot_elegido2 = slots[1]
    print(f"[LOG] Cliente selecciona segundo slot: {slot_elegido2}")
    start2 = datetime.strptime(f"2024-07-15 {slot_elegido2['start_time']}", "%Y-%m-%d %H:%M")
    end2 = datetime.strptime(f"2024-07-15 {slot_elegido2['end_time']}", "%Y-%m-%d %H:%M")
    staff_libre2 = availability_service.pick_first_free_staff(
        negocio_id=1,
        business_id=None,
        start=start2,
        end=end2
    )
    print(f"[LOG] Staff libre en el segundo intento: {staff_libre2} ({staff_repo.get_by_id(staff_libre2).name})")

print(f"""
Resumen del flujo:
- Cliente Pepe busca horarios el lunes.
- Slots: {slots}
- Intenta reservar el primero (staff: {staff_libre} - {staff_repo.get_by_id(staff_libre).name})
- Si no le gusta, prueba el segundo slot (staff: {staff_libre2 if len(slots) > 1 else 'N/A'} - {staff_repo.get_by_id(staff_libre2).name if len(slots) > 1 else 'N/A'})
- Así puede elegir horario y staff, aunque el staff solo se muestra al confirmar.
""")
