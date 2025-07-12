from typing import Optional, List

from staff.domain.entities.staff import Staff
from staff.infraestructure.models.staff_model import StaffModel


class StaffRepository:
    def get_by_id(self, id:int) -> Optional[Staff]:
        try:
            record = StaffModel.get(StaffModel.id == id)
            return Staff(
                id=record.id,
                speciality=record.speciality,
                name=record.name,
                negocio_id=record.negocio_id,
                max_capacity=record.max_capacity,
                dni=record.dni
            )
        except StaffModel.DoesNotExist:
            return None

    def list_all(self) -> List[Staff]:
        records = StaffModel.select()
        return [
            Staff(
                id=record.id,
                speciality=record.speciality,
                name=record.name,
                negocio_id=record.negocio_id,
                max_capacity=record.max_capacity,
                dni=record.dni
            ) for record in records
        ]

    def get_by_dni(self, dni: str) -> Optional[Staff]:
        try:
            record = StaffModel.get(StaffModel.dni == dni)
            return Staff(
                id=record.id,
                speciality=record.speciality,
                name=record.name,
                negocio_id=record.negocio_id,
                max_capacity=record.max_capacity,
                dni=record.dni
            )
        except StaffModel.DoesNotExist:
            return None

    def create(self, personal: Staff) -> Staff:
        record = StaffModel.create(
            speciality=personal.speciality,
            name=personal.name,
            negocio_id=personal.negocio_id,  # 👈 CORREGIDO
            max_capacity=personal.max_capacity,
            dni=personal.dni
        )
        return Staff(
            id=record.id,
            speciality=record.speciality,
            name=record.name,
            negocio_id=record.negocio_id,
            max_capacity=record.max_capacity,
            dni=record.dni
        )

    def update(self, personal: Staff) -> Staff:
        query = StaffModel.update(
            speciality=personal.speciality,
            name=personal.name,
            negocio_id=personal.negocio_id,  # 👈 CORREGIDO
            max_capacity=personal.max_capacity,
            dni=personal.dni
        ).where(StaffModel.id == personal.id)
        query.execute()
        return self.get_by_id(personal.id)

    def list_by_negocio_business(
            self,
            negocio_id: int,
            business_id: Optional[int] = None,  # Este parámetro es inútil si no existe business_id en el modelo
    ) -> List[Staff]:
        query = StaffModel.select().where(StaffModel.negocio_id == negocio_id)
        # business_id NO existe, así que no filtras por eso
        return [
            Staff(
                id=rec.id,
                speciality=rec.speciality,
                name=rec.name,
                negocio_id=rec.negocio_id,
                max_capacity=rec.max_capacity,
                dni=rec.dni,
            )
            for rec in query
        ]






















