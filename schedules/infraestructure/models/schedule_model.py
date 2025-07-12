# schedules/infraestructure/models/schedule_model.py
from peewee import Model, AutoField, CharField, TimeField, IntegerField, BooleanField, CompositeKey
from shared.infrastructure.database import db

class ScheduleModel(Model):
    id           = AutoField(primary_key=True)
    day          = CharField(null=False)           # sigue siendo string: "Monday"
    start_time   = TimeField(null=False)
    end_time     = TimeField(null=False)
    negocio_id   = IntegerField(null=False)        # <── ahora INT
    business_id  = IntegerField(null=False)        # <── ahora INT
    is_active    = BooleanField(default=True)      # <── booleano

    class Meta:
        database   = db
        table_name = 'schedules'
        indexes    = (
            (('day', 'business_id', 'negocio_id', 'is_active'), False),
        )



class ScheduleStaffModel(Model):
    staff_id    = IntegerField()
    schedule_id = IntegerField()

    class Meta:
        database     = db
        table_name   = 'schedule_staff'
        primary_key  = CompositeKey('staff_id', 'schedule_id')
