from schedules.infraestructure.models.schedule_model import ScheduleStaffModel


class ScheduleStaffRepository:

    def create(self, staff_id: int, schedule_id: int) -> bool:
        # Validar si ya existe la relación
        exists = ScheduleStaffModel.select().where(
            (ScheduleStaffModel.staff_id == staff_id) &
            (ScheduleStaffModel.schedule_id == schedule_id)
        ).exists()

        if exists:
            # Opcional: puedes lanzar una excepción, o simplemente devolver False
            return False

        ScheduleStaffModel.create(
            staff_id=staff_id,
            schedule_id=schedule_id
        )
        return True

    def delete(self,  schedule_id: int) -> bool:
        # Borra la relación antigua
        ScheduleStaffModel.delete().where(
            (ScheduleStaffModel.schedule_id == schedule_id)
        ).execute()

        return True

    def get_staff_ids_by_schedule(self, schedule_id: int) -> list:
        """
        Devuelve la lista de staff_id asociados a un horario (schedule).
        """
        query = ScheduleStaffModel.select().where(ScheduleStaffModel.schedule_id == schedule_id)
        return [rec.staff_id for rec in query]



