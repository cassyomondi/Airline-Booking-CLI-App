# migrate.py
from database import Base, engine
import models.passenger
import models.flight
import models.flight_seat
import models.booking

print("Dropping all tables...")
Base.metadata.drop_all(bind=engine)

print("Creating all tables...")
Base.metadata.create_all(bind=engine)

print("✅ Migration complete!")
