from appointment.infraestructure.repositories.appointment_repository import AppointmentRepository

class AppointmentQueryService:
    def __init__(self, appointment_repo: AppointmentRepository):
        self.appointment_repo = appointment_repo

    def get_by_id(self, appointment_id: int):
        return self.appointment_repo.get_by_id(appointment_id)

    # def list_by_client(self, client_id: int):
    #     return self.appointment_repo.list_by_client(client_id)

    def list_by_day_and_negocio(self, day: str, negocio_id: int):
        return self.appointment_repo.get_by_day_negocio_id(day, negocio_id)

    def list_by_staff_and_day(self, staff_id: int, day: str):
        return self.appointment_repo.list_by_staff_and_day(staff_id, day)
