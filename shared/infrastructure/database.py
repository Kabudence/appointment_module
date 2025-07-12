"""
Database initialization module for the Smart Band Edge Service.
"""
from peewee import MySQLDatabase
from shared.infrastructure.db_config import DB_CONFIG

# Initialize the database connection
db = MySQLDatabase(**DB_CONFIG)

def init_db() -> None:
    """
    Initialize the database connection and create the necessary tables if they do not exist.
    """
    if db.is_closed():
        db.connect()
        print("Driver usado:", type(db._state.conn))

    # Import models here to avoid circular imports
    # Import models here to avoid circular imports
    from staff.infraestructure.models.staff_model import StaffModel
    from appointment.infraestructure.models.appointment_model import AppointmentModel
    from schedules.infraestructure.models.schedule_model import ScheduleModel, ScheduleStaffModel

    db.create_tables([StaffModel, ScheduleModel, ScheduleStaffModel,AppointmentModel], safe=True)

