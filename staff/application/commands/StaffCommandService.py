from staff.domain.entities.staff import Staff
from staff.domain.services.staff_domain_service import StaffDomainService
from staff.infraestructure.repositories.staff_repository import StaffRepository


class StaffCommandService:
    """
    Service for handling personal commands.
    """

    def __init__(self, staff_repository:StaffRepository):
        self.staff_repository = staff_repository

    def create(self,
               speciality:str,
               name:str,
               negocio_id:int,
               max_capacity:int,
               dni:str) -> Staff:
        staff= Staff( speciality=speciality, name=name, negocio_id=negocio_id, max_capacity=max_capacity, dni=dni)

        all_staff = self.staff_repository.list_all()
        StaffDomainService.validate_authenticity(staff,all_staff)

        return self.staff_repository.create(staff)


    def update(self,
               id:int ,
               speciality:str,
               name:str,
               negocio_id:int,
               max_capacity:int,
               dni:str) -> Staff:
        staff = Staff(id=id, speciality=speciality, name=name, negocio_id=negocio_id, max_capacity=max_capacity,dni=dni)
        all_staff = self.staff_repository.list_all()
        StaffDomainService.validate_authenticity(staff, all_staff)
        return self.staff_repository.update(staff)