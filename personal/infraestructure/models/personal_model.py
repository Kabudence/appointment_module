from peewee import Model, CharField, IntegerField
from shared.infrastructure.database import db


class PersonalModel(Model):
    id = IntegerField(primary_key=True)
    speciality = CharField()
    name = CharField()
    business_id = IntegerField()
    max_capacity = IntegerField()

    class Meta:
        database = db
        table_name = 'personal'
