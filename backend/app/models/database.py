from sqlmodel import SQLModel, Column, DateTime, Field, Relationship
from pydantic import EmailStr
from datetime import datetime, timezone
from typing import List, Optional
from .auth import UserRole
from .reservation import ReservationStatus


# ---------- Base ----------
class BaseSQLModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)

    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True)),
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True)),
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def touch(self) -> None:
        """Refresh updated_at timestamp"""
        self.updated_at = datetime.now(timezone.utc)


# ---------- Users ----------
class User(BaseSQLModel, table=True):
    username: str = Field(index=True, unique=True, nullable=False, max_length=50)
    email: EmailStr = Field(index=True, unique=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    role: UserRole = Field(default=UserRole.USER, nullable=False)
    is_active: bool = Field(default=True, nullable=False)

    reservations: List["Reservation"] = Relationship(back_populates="user")


# ---------- Movies & Genres ----------
class Movie(BaseSQLModel, table=True):
    title: str = Field(max_length=100, nullable=False)
    description: str = Field(max_length=1000, nullable=False)
    duration_minutes: int = Field(nullable=False)
    poster_url: str = Field(nullable=True)

    genres: List["Genre"] = Relationship(back_populates="movies", link_model="MovieGenre")
    screenings: List["Screening"] = Relationship(back_populates="movie")


class Genre(BaseSQLModel, table=True):
    name: str = Field(unique=True, nullable=False)

    movies: List["Movie"] = Relationship(back_populates="genres", link_model="MovieGenre")


class MovieGenre(SQLModel, table=True):
    movie_id: int = Field(foreign_key="movie.id", primary_key=True)
    genre_id: int = Field(foreign_key="genre.id", primary_key=True)


# ---------- Theatres & Auditoriums ----------
class Theatre(BaseSQLModel, table=True):
    name: str = Field(max_length=100, nullable=False)

    auditoriums: List["Auditorium"] = Relationship(back_populates="theatre")


class Auditorium(BaseSQLModel, table=True):
    name: str = Field(max_length=100, nullable=False)
    capacity: int = Field(default=0, nullable=False)
    theatre_id: int = Field(foreign_key="theatre.id")

    theatre: "Theatre" = Relationship(back_populates="auditoriums")
    screenings: List["Screening"] = Relationship(back_populates="auditorium")
    seats: List["Seat"] = Relationship(back_populates="auditorium")


# ---------- Screenings ----------
class Screening(BaseSQLModel, table=True):
    movie_id: int = Field(foreign_key="movie.id")
    auditorium_id: int = Field(foreign_key="auditorium.id")
    start_time: datetime = Field(sa_column=Column(DateTime(timezone=True)))
    end_time: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True)))
    base_price: float = Field(gt=0, nullable=False)

    movie: "Movie" = Relationship(back_populates="screenings")
    auditorium: "Auditorium" = Relationship(back_populates="screenings")
    reservations: List["Reservation"] = Relationship(back_populates="screening")


# ---------- Seats ----------
class Seat(BaseSQLModel, table=True):
    row_label: str = Field(nullable=False)
    seat_number: int = Field(gt=0, nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    auditorium_id: int = Field(foreign_key="auditorium.id")

    auditorium: "Auditorium" = Relationship(back_populates="seats")
    reservations: List["ReservationSeat"] = Relationship(back_populates="seat")


# ---------- Reservations ----------
class Reservation(BaseSQLModel, table=True):
    status: ReservationStatus = Field(default=ReservationStatus.BOOKED, nullable=False)
    total_price: float = Field(ge=0, nullable=False)
    user_id: int = Field(foreign_key="user.id")
    screening_id: int = Field(foreign_key="screening.id")
    cancelled_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True)))

    user: "User" = Relationship(back_populates="reservations")
    screening: "Screening" = Relationship(back_populates="reservations")
    seats: List["ReservationSeat"] = Relationship(back_populates="reservation")


class ReservationSeat(SQLModel, table=True):
    reservation_id: int = Field(foreign_key="reservation.id", primary_key=True)
    seat_id: int = Field(foreign_key="seat.id", primary_key=True)
    price_paid: float = Field(gt=0, nullable=False)

    reservation: "Reservation" = Relationship(back_populates="seats")
    seat: "Seat" = Relationship(back_populates="reservations")
