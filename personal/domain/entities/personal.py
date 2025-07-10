
class Personal:
    def __init__(self,
                 id:int,
                 speciality:str,
                 name:str,
                 business_id:int,
                 max_capacity:int
                 ):
                self.id = id
                self.speciality = speciality
                self.name = name
                self.business_id = business_id
                self.max_capacity = max_capacity

                def __repr__(self):
                    return (f"Personal(id={self.id}, speciality={self.speciality},"
                            f" name={self.name}, business_id={self.business_id}, "
                            f"max_capacity={self.max_capacity})")
