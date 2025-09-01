from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///airline.db")

with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM passengers"))
    print("Passengers:")
    for row in result:
        print(row)

    result = conn.execute(text("SELECT * FROM bookings"))
    print("\nBookings:")
    for row in result:
        print(row)
