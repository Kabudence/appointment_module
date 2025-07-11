

class StaffQueryService:



    def __init__(self, staff_repository):
        self.staff_repository = staff_repository

    def get_by_id(self, staff_id: int):
        """
        Retrieve a staff member by their ID.

        :param staff_id: The ID of the staff member.
        :return: Staff object if found, None otherwise.
        """
        return self.staff_repository.get_by_id(staff_id)

    def list_all(self):
        """
        List all staff members.

        :return: List of Staff objects.
        """
        return self.staff_repository.list_all()

    def get_by_dni(self, dni: int):
        """
        Retrieve a staff member by their DNI.

        :param dni: The DNI of the staff member.
        :return: Staff object if found, None otherwise.
        """
        return self.staff_repository.get_by_dni(dni)