# models/__init__.py
from .passenger import Passenger
from .booking import Booking
from .flight import Flight
from .flight_seat import FlightSeat

__all__ = ["Passenger", "Booking", "Flight", "FlightSeat"]
