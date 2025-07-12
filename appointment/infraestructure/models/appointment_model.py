from peewee import Model, AutoField, DateTimeField, IntegerField, CharField

from appointment.domain.entities.appointment import AppointmentStatus
from shared.infrastructure.database import db

class AppointmentModel(Model):
    id = AutoField(primary_key=True)
    start_time = DateTimeField(null=False)
    end_time = DateTimeField(null=False)
    client_id = IntegerField(null=False)
    negocio_id = IntegerField(null=False)
    staff_id = IntegerField(null=False)
    status = CharField(
        max_length=20,
        default=AppointmentStatus.PENDING.value,
        choices=[(status.value, status.value) for status in AppointmentStatus]
    )
    business_id = IntegerField(null=False)
    service_id = IntegerField(null=False)

    class Meta:
        database = db
        table_name = 'appointments'
        indexes = (
            # Puedes definir índices compuestos si lo necesitas
            (('start_time', 'staff_id'), False),
        )
