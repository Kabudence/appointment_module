from peewee import Model, CharField, IntegerField, AutoField
from shared.infrastructure.database import db


class StaffModel(Model):
    id = AutoField(primary_key=True)
    speciality = CharField()
    name = CharField()
    business_id = IntegerField()
    max_capacity = IntegerField()
    dni = CharField()

    class Meta:
        database = db
        table_name = 'staff'
