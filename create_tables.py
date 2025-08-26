from database import Base, engine
from models.flight import Flight
# import other models later

print("Creating tables...")
Base.metadata.create_all(engine)
print("Tables created successfully!")
