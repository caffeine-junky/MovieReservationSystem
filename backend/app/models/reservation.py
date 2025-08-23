from enum import StrEnum


class ReservationStatus(StrEnum):
    BOOKED = "booked"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    EXPIRED = "expired"

