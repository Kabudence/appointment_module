from typing import Optional, List

from personal.infraestructure.models.personal_model import PersonalModel


class PersonalRepository:
    def get_by_id(self, id:int) -> Optional[PersonalModel]:
        try:
            record = PersonalModel.get(PersonalModel.id == id)
            return PersonalModel(
                id=record.id,
                speciality=record.speciality,
                name=record.name,
                business_id=record.business_id,
                max_capacity=record.max_capacity
            )
        except PersonalModel.DoesNotExist:
            return None

    def list_all(self) -> List[PersonalModel]:
        records = PersonalModel.select()
        return [
            PersonalModel(
                id=record.id,
                speciality=record.speciality,
                name=record.name,
                business_id=record.business_id,
                max_capacity=record.max_capacity
            ) for record in records
        ]

    def create(self, personal: PersonalModel) -> PersonalModel:
        record = PersonalModel.create(
            speciality=personal.speciality,
            name=personal.name,
            business_id=personal.business_id,
            max_capacity=personal.max_capacity
        )
        return PersonalModel(
            id=record.id,
            speciality=record.speciality,
            name=record.name,
            business_id=record.business_id,
            max_capacity=record.max_capacity
        )