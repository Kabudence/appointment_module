from datetime import datetime, timedelta, time

from typing import List, Dict, Any

def str_to_time(hhmm: str) -> time:
    return datetime.strptime(hhmm, "%H:%M").time()

def time_to_minutes(t: time) -> int:
    return t.hour * 60 + t.minute

def minutes_to_time(mins: int) -> time:
    return (datetime.min + timedelta(minutes=mins)).time()


def find_available_slots(schedule, duration_minutes: int, occupied_slots: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    sched_start = str_to_time(schedule.start_time) if isinstance(schedule.start_time, str) else schedule.start_time
    sched_end   = str_to_time(schedule.end_time) if isinstance(schedule.end_time, str) else schedule.end_time

    occupied = sorted(occupied_slots, key=lambda x: str_to_time(x['start_time']))
    free_blocks = []
    curr_start = sched_start
    
    for slot in occupied:
        occ_start = str_to_time(slot['start_time'])
        occ_end   = str_to_time(slot['end_time'])

        occ_end_plus = minutes_to_time(time_to_minutes(occ_end) + 1)

        diff = time_to_minutes(occ_start) - time_to_minutes(curr_start)
        if diff >= duration_minutes:
            free_blocks.extend(all_subslots_contiguous(curr_start, occ_start, duration_minutes))
        curr_start = max(curr_start, occ_end_plus)  # Avanza un minuto después de la cita ocupada

    diff = time_to_minutes(sched_end) - time_to_minutes(curr_start)
    if diff >= duration_minutes:
        free_blocks.extend(all_subslots_contiguous(curr_start, sched_end, duration_minutes))

    return free_blocks


def all_subslots_contiguous(start: time, end: time, duration: int) -> List[Dict[str, str]]:
    """
    Devuelve TODOS los sub-bloques posibles de duración `duration` (en minutos) entre start y end,
    SIN solaparse (uno tras otro, tipo agenda tradicional).
    """
    slots = []
    start_min = time_to_minutes(start)
    end_min = time_to_minutes(end)
    actual = start_min
    while actual + duration <= end_min:
        slot_start = minutes_to_time(actual)
        slot_end = minutes_to_time(actual + duration)
        slots.append({
            'start_time': slot_start.strftime("%H:%M"),
            'end_time': slot_end.strftime("%H:%M")
        })
        actual += duration  # Salta al siguiente bloque contiguo
    return slots

