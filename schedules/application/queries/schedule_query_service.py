from typing import Optional, List

from schedules.domain.entities.schedule import Schedule
from schedules.infraestructure.repositories.schedule_repository import ScheduleRepository


class ScheduleQueryService:

    def __init__(self, schedule_repository: ScheduleRepository):
        self.schedule_repository = schedule_repository


    def get_by_negocio_business_and_day(self, negocio_id: int, business_id: int, day: str) -> Schedule:
            schedule = self.schedule_repository.get_by_day_and_business_and_negocio(day=day, business_id=business_id,
                                                                                    negocio_id=negocio_id)
            if not schedule:
                raise ValueError(f"No schedule found for day {day}, business {business_id} and negocio {negocio_id}.")
            return schedule


    def get_schedule_with_staff_by_negocio_business_and_day(self, negocio_id: int, business_id: int, day: str):
        result = self.schedule_repository.get_schedule_with_staff(
            day=day,
            business_id=business_id,
            negocio_id=negocio_id
        )
        if not result:
            raise ValueError(f"No schedule+staff found for day {day}, business {business_id} and negocio {negocio_id}.")
        return result


    def get_all_days_by_negocio_business(self, negocio_id: int, business_id: Optional[int] = None) -> List[Schedule]:
        """
        Retrieve all days with schedules for a specific negocio and business.

        :param negocio_id: The ID of the negocio.
        :param business_id: The ID of the business.
        :return: List of days with schedules.
        """
        return self.schedule_repository.get_by_negocio_and_businessl(negocio_id=negocio_id, business_id=business_id)
