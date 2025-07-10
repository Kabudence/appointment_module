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
                business_id=record.business_id,
                max_capacity=record.max_capacity
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
                business_id=record.business_id,
                max_capacity=record.max_capacity
            ) for record in records
        ]

    def create(self, personal: Staff) -> Staff:
        record = StaffModel.create(
            speciality=personal.speciality,
            name=personal.name,
            business_id=personal.business_id,
            max_capacity=personal.max_capacity
        )
        return Staff(
            id=record.id,
            speciality=record.speciality,
            name=record.name,
            business_id=record.business_id,
            max_capacity=record.max_capacity
        )

    def update(self, personal: Staff) -> Staff:
        query = StaffModel.update(
            speciality=personal.speciality,
            name=personal.name,
            business_id=personal.business_id,
            max_capacity=personal.max_capacity
        ).where(StaffModel.id == personal.id)
        query.execute()
        return self.get_by_id(personal.id)






















