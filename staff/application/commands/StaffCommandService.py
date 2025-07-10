from staff.domain.entities.staff import Staff
from staff.infraestructure.repositories.staff_repository import StaffRepository


class PersonalCommandService:
    """
    Service for handling personal commands.
    """

    def __init__(self, staff_repository:StaffRepository):
        self.staff_repository = staff_repository

    def create(self,
               id:int ,
               speciality:str,
               name:str,
               business_id:int,
               max_capacity:int) -> Staff:
        staff= Staff(id=id, speciality=speciality, name=name, business_id=business_id, max_capacity=max_capacity)
        return self.staff_repository.create(staff)
