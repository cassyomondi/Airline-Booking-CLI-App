from database import Base, engine
from models.passenger import Passenger
from models.flight import Flight
from models.flight_seat import FlightSeat
from models.booking import Booking

print("Creating tables...")
Base.metadata.create_all(engine)
print("Tables created successfully!")
