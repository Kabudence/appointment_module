from peewee import Model, CharField, IntegerField, AutoField
from shared.infrastructure.database import db


class StaffModel(Model):
    id = AutoField(primary_key=True)
    speciality = CharField()
    name = CharField()
    negocio_id = IntegerField()
    max_capacity = IntegerField()
    dni = CharField(max_length=20, unique=True)
    class Meta:
        database = db
        table_name = 'staff'
