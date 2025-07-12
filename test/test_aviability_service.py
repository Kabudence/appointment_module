from datetime import datetime, timedelta

from appointment.domain.services.availability_service import AvailabilityService

# Simulamos las dependencias (repos y función)
class FakeScheduleRepo:
    def get_by_day_and_business_and_negocio(self, day, business_id, negocio_id):
        from schedules.domain.entities.schedule import Schedule
        print(f"[ScheduleRepo] get_by_day_and_business_and_negocio(day={day}, business_id={business_id}, negocio_id={negocio_id})")
        return Schedule(day=day, start_time="08:00", end_time="22:00", negocio_id=negocio_id, business_id=business_id)

class FakeStaffRepo:
    def list_by_negocio_business(self, negocio_id, business_id):
        from staff.domain.entities.staff import Staff
        print(f"[StaffRepo] list_by_negocio_business(negocio_id={negocio_id}, business_id={business_id})")
        return [
            Staff(id=1, speciality="Dentista", name="Ana", business_id=business_id, max_capacity=10, dni="1111"),
            Staff(id=2, speciality="Odontologo", name="Pepe", business_id=business_id, max_capacity=10, dni="2222")
        ]

class FakeAppointment:
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time

class FakeAppointmentRepo:
    def __init__(self):
        self.citas = {
            1: [FakeAppointment(datetime(2024,7,12,10,0), datetime(2024,7,12,11,0))],
            2: []
        }
    def list_by_staff_and_day(self, staff_id, day):
        print(f"[AppointmentRepo] list_by_staff_and_day(staff_id={staff_id}, day={day}) -> citas: {len(self.citas.get(staff_id, []))}")
        return self.citas.get(staff_id, [])
    def is_staff_free(self, staff_id, start, end):
        print(f"[AppointmentRepo] is_staff_free(staff_id={staff_id}, start={start}, end={end})")
        for c in self.citas.get(staff_id, []):
            print(f"   - Comparando con cita: {c.start_time} a {c.end_time}")
            if not (end <= c.start_time or start >= c.end_time):
                print("   -> Staff ocupado en ese horario")
                return False
        print("   -> Staff libre en ese horario")
        return True

# Mock para find_available_slots
def fake_find_available_slots(schedule, duration_min, occupied):
    print(f"[find_available_slots] Llamada con occupied={occupied}")
    return [{"start_time": "11:00", "end_time": "12:00"}]

def test_find_available_slots_for_day():
    print("\n==== Test: find_available_slots_for_day ====")
    from schedules.domain.services.schedule_service import find_available_slots  # Normalmente import real aquí

    service = AvailabilityService(
        schedule_repo=FakeScheduleRepo(),
        staff_repo=FakeStaffRepo(),
        appointment_repo=FakeAppointmentRepo()
    )

    # PARCHA la función
    service.find_available_slots = fake_find_available_slots

    result = service.find_available_slots_for_day(
        negocio_id=1,
        business_id=101,
        day="2024-07-12",
        service_duration_min=60
    )

    print("=> Resultado Slots disponibles:", result)
    assert isinstance(result, list)
    assert any(slot["start_time"] == "11:00" for slot in result)

def test_pick_first_free_staff():
    print("\n==== Test: pick_first_free_staff ====")
    service = AvailabilityService(
        schedule_repo=FakeScheduleRepo(),
        staff_repo=FakeStaffRepo(),
        appointment_repo=FakeAppointmentRepo()
    )

    free_staff = service.pick_first_free_staff(
        negocio_id=1,
        business_id=101,
        start=datetime(2024,7,12,10,0),
        end=datetime(2024,7,12,11,0)
    )
    print("=> Staff libre encontrado:", free_staff)
    assert free_staff == 2

if __name__ == "__main__":
    test_find_available_slots_for_day()
    test_pick_first_free_staff()
    print("\n✅ Todos los tests pasaron correctamente.")
