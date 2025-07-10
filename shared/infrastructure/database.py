"""
Database initialization module for the Smart Band Edge Service.
"""
from peewee import SqliteDatabase



# Initialize the database connection
db = SqliteDatabase('test_appointment_db.db')

def init_db() -> None:
    """
    Initialize the database connection. It also creates the necessary tables if they do not exist.
    """
    db.connect()
    """ 
    Create tables if they do not exist.
    """
    # from health.infrastructure.models import HealthRecord
    # from iam.infrastructure.models import Device
    # db.create_tables([Device, HealthRecord], safe=True)  # Replace with actual model classes when defined
