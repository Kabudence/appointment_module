class Schedule:
    def __init__(self,
                 id: int = None,
                 day: str = "",
                 start_time: str = "",
                 end_time: str = "",
                 negocio_id: int = None,
                 business_id: int = None,
                 is_active: bool = True,
                 ):
        self.id = id
        self.day = day
        self.start_time = start_time
        self.end_time = end_time
        self.negocio_id = negocio_id
        self.business_id = business_id
        self.is_active = is_active


    def to_dict(self):
        return {
            "id": self.id,
            "day": self.day,
            "start_time": self.start_time.strftime("%H:%M") if hasattr(self.start_time, "strftime") else self.start_time,
            "end_time": self.end_time.strftime("%H:%M") if hasattr(self.end_time, "strftime") else self.end_time,
            "negocio_id": self.negocio_id,
            "business_id": self.business_id,
            "is_active": self.is_active
        }