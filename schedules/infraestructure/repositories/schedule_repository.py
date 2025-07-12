from typing import Optional, List, Dict, Any

from schedules.domain.entities.schedule import Schedule
from schedules.infraestructure.models.schedule_model import ScheduleModel,ScheduleStaffModel
from staff.infraestructure.models.staff_model import StaffModel


class ScheduleRepository:
    def get_by_id(self, id:int) -> Optional[Schedule]:
        try:
            record = ScheduleModel.get(ScheduleModel.id == id)
            return Schedule(
                id=record.id,
                day=record.day,
                start_time=record.start_time,
                end_time=record.end_time,
                negocio_id=record.negocio_id,
                business_id=record.business_id,
                is_active=record.is_active
            )
        except ScheduleModel.DoesNotExist:
            return None

    def get_by_day_and_business_and_negocio(self, day: str, business_id: int, negocio_id: int) -> Optional[Schedule]:
        try:
            record = (ScheduleModel.
                      get((ScheduleModel.day == day) &
                          (ScheduleModel.business_id == business_id) &
                          (ScheduleModel.negocio_id == negocio_id)&
                             ScheduleModel.is_active == True))
            return Schedule(
                id=record.id,
                day=record.day,
                start_time=record.start_time,
                end_time=record.end_time,
                negocio_id=record.negocio_id,
                business_id=record.business_id,
                is_active=record.is_active
            )
        except ScheduleModel.DoesNotExist:
            return None

    def get_by_negocio_and_businessl(self, negocio_id: Optional[int] = None, business_id: Optional[int] = None) -> List[Schedule]:
        query = ScheduleModel.select()
        if negocio_id is not None:
            query = query.where(ScheduleModel.negocio_id == negocio_id)
        if business_id is not None:
            query = query.where(ScheduleModel.business_id == business_id)

        # Devuelve lista (puede estar vacía)
        return [
            Schedule(
                id=record.id,
                day=record.day,
                start_time=record.start_time,
                end_time=record.end_time,
                negocio_id=record.negocio_id,
                business_id=record.business_id,
                is_active=record.is_active
            )
            for record in query
        ]

    def get_relationships_by_staff_or_schedule(self,
                                               staff_id: Optional[str] = None,
                                               schedule_id: Optional[str] = None
                                               ) -> List[ScheduleStaffModel]:

        query = ScheduleStaffModel.select()
        if staff_id is not None:
            query = query.where(ScheduleStaffModel.staff_id == staff_id)
        if schedule_id is not None:
            query = query.where(ScheduleStaffModel.schedule_id == schedule_id)
        return list(query)

    def get_schedule_with_staff(self, day: str, business_id: int, negocio_id: int) -> Optional[Dict[str, Any]]:
        try:
            # 1. Encuentra el schedule principal
            schedule_record = (ScheduleModel
                               .get((ScheduleModel.day == day) &
                                    (ScheduleModel.business_id == business_id) &
                                    (ScheduleModel.negocio_id == negocio_id) &
                                    (ScheduleModel.is_active == True)))
            # 2. Trae todos los staff asociados a ese schedule usando JOIN
            staff_query = (StaffModel
                           .select()
                           .join(ScheduleStaffModel, on=(StaffModel.id == ScheduleStaffModel.staff_id))
                           .where(ScheduleStaffModel.schedule_id == schedule_record.id))
            staff_list = [{
                "id": s.id,
                "speciality": s.speciality,
                "name": s.name,
                "negocio_id": s.negocio_id,
                "max_capacity": s.max_capacity,
                "dni": getattr(s, "dni", None)
            } for s in staff_query]

            # 3. Devuelve un dict con los datos combinados
            return {
                "schedule": {
                    "id": schedule_record.id,
                    "day": schedule_record.day,
                    "start_time": schedule_record.start_time.strftime("%H:%M"),
                    "end_time": schedule_record.end_time.strftime("%H:%M"),
                    "negocio_id": schedule_record.negocio_id,
                    "business_id": schedule_record.business_id,
                    "is_active": schedule_record.is_active
                },
                "staff": staff_list
            }
        except ScheduleModel.DoesNotExist:
            return None



    def create(self, schedule: Schedule) -> Schedule:
        record = ScheduleModel.create(
            day=schedule.day,
            start_time=schedule.start_time,
            end_time=schedule.end_time,
            negocio_id=schedule.negocio_id,
            business_id=schedule.business_id,
            is_active=schedule.is_active
        )
        return Schedule(
            id=record.id,
            day=record.day,
            start_time=record.start_time,
            end_time=record.end_time,
            negocio_id=record.negocio_id,
            business_id=record.business_id,
            is_active=record.is_active
        )
    def update(self, schedule: Schedule) -> Schedule:
        record = ScheduleModel.get(ScheduleModel.id == schedule.id)
        record.day = schedule.day
        record.start_time = schedule.start_time
        record.end_time = schedule.end_time
        record.negocio_id = schedule.negocio_id
        record.business_id = schedule.business_id
        record.is_active = schedule.is_active
        record.save()
        return Schedule(
            id=record.id,
            day=record.day,
            start_time=record.start_time,
            end_time=record.end_time,
            negocio_id=record.negocio_id,
            business_id=record.business_id,
            is_active=record.is_active
        )

