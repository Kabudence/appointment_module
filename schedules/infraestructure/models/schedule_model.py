from peewee import Model, AutoField, CharField, TimeField
from shared.infrastructure.database import db


class ScheduleModel(Model):
    id = AutoField(primary_key=True)
    day = CharField(null=False)
    start_time = TimeField(null=False)
    end_time = TimeField(null=False)
    negocio_id = CharField(null=False)
    business_id = CharField(null=False)
    is_active = CharField(null=False)

    class Meta:
        database = db
        table_name = 'schedules'
        indexes = (
            # Indice compuesto
            (('day', 'business_id', 'negocio_id', 'is_active'), False),  # False = no único
        )

from peewee import Model, CharField, CompositeKey
from shared.infrastructure.database import db

class ScheduleStaffModel(Model):
    staff_id = CharField()
    schedule_id = CharField()

    class Meta:
        database = db
        table_name = 'schedule_staff'
        primary_key = CompositeKey('staff_id', 'schedule_id')
