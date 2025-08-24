from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint, Index
from sqlalchemy import DateTime, Numeric, CheckConstraint
from pydantic import EmailStr, field_validator
from decimal import Decimal
from datetime import datetime, timezone
from typing import Any, List, Optional
from .auth import UserRole
from .reservation import ReservationStatus


# ---------- Base ----------
class BaseSQLModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)

    created_at: datetime = Field(
        sa_type=DateTime(timezone=True), # type: ignore
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        sa_type=DateTime(timezone=True), # type: ignore
        default_factory=lambda: datetime.now(timezone.utc),
    )
    
    # Soft delete support
    deleted_at: Optional[datetime] = Field(
        default=None, 
        sa_type=DateTime(timezone=True) # type: ignore
    )

    def touch(self) -> None:
        """Refresh updated_at timestamp"""
        self.updated_at = datetime.now(timezone.utc)
    
    @property
    def is_deleted(self) -> bool:
        """Check if record is soft deleted"""
        return self.deleted_at is not None
    
    def soft_delete(self) -> None:
        """Mark record as deleted"""
        self.deleted_at = datetime.now(timezone.utc)
        self.touch()


# ---------- Users ----------
class User(BaseSQLModel, table=True):
    __table_args__ = (
        Index('idx_user_email_active', 'email', 'is_active'),
        Index('idx_user_username_active', 'username', 'is_active'),
    )
    
    username: str = Field(index=True, unique=True, max_length=50)
    email: EmailStr = Field(index=True, unique=True)
    hashed_password: str
    role: UserRole = Field(default=UserRole.USER, index=True)
    is_active: bool = Field(default=True, index=True)

    # Relationships
    reservations: List["Reservation"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "select"}
    )


# ---------- Movies & Genres ----------
class MovieGenre(SQLModel, table=True):
    movie_id: int = Field(foreign_key="movie.id", primary_key=True)
    genre_id: int = Field(foreign_key="genre.id", primary_key=True)


class Movie(BaseSQLModel, table=True):
    __table_args__ = (
        Index('idx_movie_title', 'title'),
        CheckConstraint('duration_minutes > 0', name='chk_movie_duration_positive'),
    )
    
    title: str = Field(max_length=200)
    description: str = Field(max_length=2000)
    duration_minutes: int = Field(gt=0)
    poster_url: Optional[str] = Field(default=None, max_length=500)
    is_active: bool = Field(default=True, index=True)  # For hiding movies
    
    # genre_names: Optional[str] = Field(default=None, max_length=200)

    # Relationships
    genres: List["Genre"] = Relationship(
        back_populates="movies", 
        link_model=MovieGenre,
        sa_relationship_kwargs={"lazy": "select"}
    )
    screenings: List["Screening"] = Relationship(
        back_populates="movie",
        sa_relationship_kwargs={"lazy": "select"}
    )


class Genre(BaseSQLModel, table=True):
    name: str = Field(unique=True, max_length=50)
    is_active: bool = Field(default=True, index=True)

    # Relationships
    movies: List["Movie"] = Relationship(
        back_populates="genres", 
        link_model=MovieGenre,
        sa_relationship_kwargs={"lazy": "select"}
    )


# ---------- Theatres & Auditoriums ----------
class Theatre(BaseSQLModel, table=True):
    __table_args__ = (
        Index('idx_theatre_name', 'name'),
    )
    
    name: str = Field(max_length=200)
    address: Optional[str] = Field(default=None, max_length=500)  # Added address
    is_active: bool = Field(default=True, index=True)

    # Relationships
    auditoriums: List["Auditorium"] = Relationship(
        back_populates="theatre",
        sa_relationship_kwargs={"lazy": "select"}
    )


class Auditorium(BaseSQLModel, table=True):
    __table_args__ = (
        UniqueConstraint('theatre_id', 'name', name='uq_auditorium_theatre_name'),
        CheckConstraint('capacity >= 0', name='chk_auditorium_capacity_non_negative'),
        Index('idx_auditorium_theatre', 'theatre_id'),
    )
    
    name: str = Field(max_length=100)
    capacity: int = Field(ge=0, default=0)
    is_active: bool = Field(default=True, index=True)
    theatre_id: int = Field(foreign_key="theatre.id", index=True)

    # Relationships
    theatre: "Theatre" = Relationship(back_populates="auditoriums")
    screenings: List["Screening"] = Relationship(
        back_populates="auditorium",
        sa_relationship_kwargs={"lazy": "select"}
    )
    seats: List["Seat"] = Relationship(
        back_populates="auditorium",
        sa_relationship_kwargs={"lazy": "select"}
    )


# ---------- Screenings ----------
class Screening(BaseSQLModel, table=True):
    __table_args__ = (
        # Prevent overlapping screenings in same auditorium
        Index('idx_screening_auditorium_time', 'auditorium_id', 'start_time', 'end_time'),
        Index('idx_screening_movie_time', 'movie_id', 'start_time'),
        Index('idx_screening_start_time', 'start_time'),
        CheckConstraint('base_price > 0', name='chk_screening_price_positive'),
        CheckConstraint('end_time > start_time', name='chk_screening_end_after_start'),
    )
    
    movie_id: int = Field(foreign_key="movie.id", index=True)
    auditorium_id: int = Field(foreign_key="auditorium.id", index=True)
    start_time: datetime = Field(sa_type=DateTime(timezone=True), index=True) # type: ignore
    end_time: datetime = Field(sa_type=DateTime(timezone=True)) # type: ignore
    base_price: Decimal = Field(
        sa_type=Numeric(10, 2), # type: ignore
        gt=0,
        description="Base ticket price in currency units"
    )
    is_active: bool = Field(default=True, index=True)
    
    # Denormalized fields for performance
    available_seats: int = Field(default=0, ge=0)

    # Relationships
    movie: "Movie" = Relationship(back_populates="screenings")
    auditorium: "Auditorium" = Relationship(back_populates="screenings")
    reservations: List["Reservation"] = Relationship(
        back_populates="screening",
        sa_relationship_kwargs={"lazy": "select"}
    )

    @field_validator('end_time')
    def validate_end_time(cls, v: Any, values: Any):
        if v and values.get('start_time') and v <= values['start_time']:
            raise ValueError('End time must be after start time')
        return v

    @field_validator('start_time')
    def validate_start_time_future(cls, v: Any):
        if v and v <= datetime.now(timezone.utc):
            raise ValueError('Start time must be in the future')
        return v


# ---------- Seats ----------
class Seat(BaseSQLModel, table=True):
    __table_args__ = (
        UniqueConstraint('auditorium_id', 'row_label', 'seat_number', 
                        name='uq_seat_auditorium_position'),
        Index('idx_seat_auditorium', 'auditorium_id'),
        CheckConstraint('seat_number > 0', name='chk_seat_number_positive'),
    )
    
    row_label: str = Field(max_length=5)  # A, B, C, etc.
    seat_number: int = Field(gt=0)
    is_active: bool = Field(default=True, index=True)
    seat_type: Optional[str] = Field(default="standard", max_length=20)  # standard, premium, etc.
    auditorium_id: int = Field(foreign_key="auditorium.id", index=True)

    # Relationships
    auditorium: "Auditorium" = Relationship(back_populates="seats")
    reservations: List["ReservationSeat"] = Relationship(
        back_populates="seat",
        sa_relationship_kwargs={"lazy": "select"}
    )

    @property
    def seat_identifier(self) -> str:
        """Human readable seat identifier like 'A12'"""
        return f"{self.row_label}{self.seat_number}"


# ---------- Reservations ----------
class Reservation(BaseSQLModel, table=True):
    __table_args__ = (
        Index('idx_reservation_user_status', 'user_id', 'status'),
        Index('idx_reservation_screening', 'screening_id'),
        Index('idx_reservation_status', 'status'),
        CheckConstraint('total_price >= 0', name='chk_reservation_total_non_negative'),
    )
    
    status: ReservationStatus = Field(default=ReservationStatus.BOOKED, index=True)
    total_price: Decimal = Field(
        sa_type=Numeric(10, 2), # type: ignore
        ge=0,
        description="Total amount paid for reservation"
    )
    user_id: int = Field(foreign_key="user.id", index=True)
    screening_id: int = Field(foreign_key="screening.id", index=True)
    cancelled_at: Optional[datetime] = Field(
        default=None, 
        sa_type=DateTime(timezone=True) # type: ignore
    )
    
    # Additional fields
    booking_reference: Optional[str] = Field(default=None, unique=True, max_length=20)
    notes: Optional[str] = Field(default=None, max_length=500)

    # Relationships
    user: "User" = Relationship(back_populates="reservations")
    screening: "Screening" = Relationship(back_populates="reservations")
    seats: List["ReservationSeat"] = Relationship(
        back_populates="reservation",
        sa_relationship_kwargs={"lazy": "select"}
    )

    def cancel(self) -> None:
        """Cancel the reservation"""
        self.status = ReservationStatus.CANCELLED
        self.cancelled_at = datetime.now(timezone.utc)
        self.touch()

    @property
    def is_cancelled(self) -> bool:
        return self.status == ReservationStatus.CANCELLED


class ReservationSeat(SQLModel, table=True):
    __table_args__ = (
        Index('idx_reservation_seat_reservation', 'reservation_id'),
        Index('idx_reservation_seat_seat', 'seat_id'),
        CheckConstraint('price_paid >= 0', name='chk_reservation_seat_price_non_negative'),
    )
    
    reservation_id: int = Field(foreign_key="reservation.id", primary_key=True)
    seat_id: int = Field(foreign_key="seat.id", primary_key=True)
    price_paid: Decimal = Field(
        sa_type=Numeric(10, 2), # type: ignore
        ge=0,  # Changed from gt=0 to allow free tickets
        description="Amount paid for this specific seat"
    )

    # Relationships
    reservation: "Reservation" = Relationship(back_populates="seats")
    seat: "Seat" = Relationship(back_populates="reservations")
