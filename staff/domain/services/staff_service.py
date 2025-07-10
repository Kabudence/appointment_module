class PersonalDomainService:
    @staticmethod
    def validate_authenticity(staff,other_staff):
        for other in other_staff:
            if staff.id == other.id and \
                staff.name == other.name:
                raise ValueError(f"Staff with ID {staff.id} and name {staff.name} already exists.")