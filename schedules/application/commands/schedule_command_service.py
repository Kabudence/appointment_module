from typing import List, Union

from schedules.domain.entities.schedule import Schedule
from schedules.infraestructure.repositories.schedule_repository import ScheduleRepository
from schedules.infraestructure.repositories.schedule_staff_repository import ScheduleStaffRepository


class ScheduleCommandService:
    def __init__(self,  schedule_repository:ScheduleRepository, schedule_staff_repository:ScheduleStaffRepository):
        self.schedule_repository = schedule_repository
        self.schedule_staff_repository = schedule_staff_repository


    def create(self,
               day: str,
               start_time: str,
               end_time: str,
               negocio_id: int,
               business_id: int,
               staff_ids: Union[int, List[int]]
               ) -> Schedule:
        schedule = Schedule(
            day=day,
            start_time=start_time,
            end_time=end_time,
            negocio_id=negocio_id,
            business_id=business_id
        )
        existing_schedule = self.schedule_repository.get_by_day_and_business_and_negocio(
            day=day, business_id=business_id, negocio_id=negocio_id)
        if existing_schedule:
            raise ValueError(
                f"Schedule for day {day}, business {business_id} and negocio {negocio_id} already exists."
            )
        new_schedule = self.schedule_repository.create(schedule)

        self._create_staff_relationships(new_schedule.id, staff_ids)

        return new_schedule

    def update(self,
               schedule_id: int,
               day: str,
               start_time: str,
               end_time: str,
               negocio_id: int,
               business_id: int,
               staff_ids: Union[int, List[int]]
               ) -> Schedule:

        # 1. Actualiza el horario principal
        schedule = Schedule(
            id=schedule_id,
            day=day,
            start_time=start_time,
            end_time=end_time,
            negocio_id=negocio_id,
            business_id=business_id
        )
        existing_schedule = self.schedule_repository.get_by_id(schedule_id)
        if not existing_schedule:
            raise ValueError(f"Schedule with id {schedule_id} not found.")

        updated_schedule = self.schedule_repository.update(schedule)

        self.schedule_staff_repository.delete(schedule_id)


        self._create_staff_relationships(updated_schedule.id, staff_ids)

        return updated_schedule



    def _create_staff_relationships(self, schedule_id: int, staff_ids: Union[int, List[int]]) -> None:
        """
        Crea relaciones schedule-staff para una lista de staff_ids. Lanza error si ya existen.
        """
        # Permite aceptar uno o varios staff_id
        if isinstance(staff_ids, int):
            staff_ids = [staff_ids]
        errores = []
        for staff_id in staff_ids:
            if not self.schedule_staff_repository.create(staff_id, schedule_id):
                errores.append(staff_id)
        if errores:
            raise ValueError(
                f"Schedule-staff relationship already exists for staff IDs: {errores} and schedule {schedule_id}"
            )