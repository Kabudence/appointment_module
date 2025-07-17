# Ejemplo de schedule de 8:00 a 22:00
from schedules.domain.entities.schedule import Schedule
from schedules.domain.services.schedule_service import find_available_slots

schedule = Schedule(start_time="08:00", end_time="22:00")
duration = 120

occupied_slots = [
    {'start_time': '08:00', 'end_time': '09:10'},
    {'start_time': '09:35', 'end_time': '11:14'},
    {'start_time': '16:20', 'end_time': '18:00'},
]

free_slots = find_available_slots(schedule, duration, occupied_slots)
print(free_slots)
