class Staff:
    def __init__(self,
                 id: int = None,  # Haz id opcional para creación (cuando aún no existe)
                 speciality: str = "",
                 name: str = "",
                 business_id: int = 0,
                 max_capacity: int = 0,
                 dni: str = ""
                 ):
        self.id = id
        self.speciality = speciality
        self.name = name
        self.business_id = business_id
        self.max_capacity = max_capacity
        self.dni = dni

    def __repr__(self):
        return (f"Staff(id={self.id}, speciality={self.speciality},"
                f" name={self.name}, business_id={self.business_id}, "
                f"max_capacity={self.max_capacity}, dni={self.dni})")
