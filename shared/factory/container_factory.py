# container.py
from appointment.infraestructure.repositories.appointment_repository import AppointmentRepository
from appointment.application.commands.appointment_command_service import AppointmentCommandService
from appointment.application.queries.appointment_query_service import AppointmentQueryService
from appointment.application.queries.availability_query_service import AvailabilityQueryService
from appointment.domain.services.availability_service import AvailabilityService
from schedules.application.commands.schedule_command_service import ScheduleCommandService
from schedules.application.queries.schedule_query_service import ScheduleQueryService

from schedules.infraestructure.repositories.schedule_repository import ScheduleRepository
from schedules.infraestructure.repositories.schedule_staff_repository import ScheduleStaffRepository

from staff.infraestructure.repositories.staff_repository import StaffRepository
from staff.application.commands.StaffCommandService import StaffCommandService
from staff.application.queries.StaffQueryService import StaffQueryService
def build_services():
    # ---------- Repos ----------
    appointment_repo   = AppointmentRepository()
    schedule_repo      = ScheduleRepository()
    schedule_staff_repo= ScheduleStaffRepository()
    staff_repo         = StaffRepository()

    # ---------- Services ----------
    # SCHEDULE
    schedule_command_service = ScheduleCommandService(schedule_repo, schedule_staff_repo)
    schedule_query_service   = ScheduleQueryService(schedule_repo)

    # APPOINTMENT
    appointment_command_service = AppointmentCommandService(appointment_repo)
    appointment_query_service   = AppointmentQueryService(appointment_repo)

    # STAFF
    staff_command_service = StaffCommandService(staff_repo)
    staff_query_service   = StaffQueryService(staff_repo)

    # AVAILABILITY
    availability_service       = AvailabilityService(
        schedule_repo, schedule_staff_repo, staff_repo, appointment_repo
    )
    availability_query_service = AvailabilityQueryService(availability_service)

    # ---------- Registro en app.config ----------
    return {
        # schedule
        "schedule_command_service": schedule_command_service,
        "schedule_query_service"  : schedule_query_service,

        # appointment
        "appointment_command_service": appointment_command_service,
        "appointment_query_service"  : appointment_query_service,

        # staff
        "staff_command_service": staff_command_service,
        "staff_query_service"  : staff_query_service,

        # availability
        "availability_service"       : availability_service,
        "availability_query_service" : availability_query_service,

        # repos (por si algún endpoint los necesita)
        "schedule_repo"      : schedule_repo,
        "schedule_staff_repo": schedule_staff_repo,
        "appointment_repo"   : appointment_repo,
        "staff_repo"         : staff_repo,
    }