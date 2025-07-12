from datetime import datetime
from enum import Enum

class AppointmentStatus(Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    NO_SHOW = "NO_SHOW"

class Appointment:
    def __init__(
        self,
        id: int = None,
        start_time: datetime = None,
        end_time: datetime = None,
        client_id: int = None,
        negocio_id: int = None,
        staff_id: int = None,
        status: AppointmentStatus = AppointmentStatus.PENDING,
        business_id: int = None,
        service_id: int = None,
    ):
        self.id = id
        self.start_time = start_time
        self.end_time = end_time
        self.client_id = client_id
        self.negocio_id = negocio_id
        self.staff_id = staff_id
        self.status = status
        self.business_id = business_id
        self.service_id = service_id

    def __repr__(self):
        return (
            f"<Appointment(id={self.id}, start_time={self.start_time}, end_time={self.end_time}, "
            f"client_id={self.client_id}, business_id={self.business_id}, staff_id={self.staff_id}, "
            f"status={self.status}, location_id={self.business_id}, service_id={self.service_id})>"
        )


    def to_dict(self) -> dict:
        return {
            "id"         : self.id,
            "start_time" : self.start_time.isoformat() if isinstance(self.start_time, datetime) else self.start_time,
            "end_time"   : self.end_time.isoformat()   if isinstance(self.end_time,   datetime) else self.end_time,
            "client_id"  : self.client_id,
            "negocio_id" : self.negocio_id,
            "staff_id"   : self.staff_id,
            "status"     : self.status.value if isinstance(self.status, AppointmentStatus) else self.status,
            "business_id": self.business_id,
            "service_id" : self.service_id,
        }
