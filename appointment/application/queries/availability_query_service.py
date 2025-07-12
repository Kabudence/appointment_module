# appointment/application/queries/availability_query_service.py
class AvailabilityQueryService:
    def __init__(self, availability_service):
        self.availability_service = availability_service

    def get_available_slots(self, negocio_id, business_id, day, duration):
        return self.availability_service.find_available_slots_for_day(
            negocio_id, business_id, day, duration
        )
