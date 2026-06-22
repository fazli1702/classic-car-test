import json
from pathlib import Path
from dotenv import load_dotenv
import os

from sqlalchemy import create_engine, String, Text, Boolean, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
DATABASE_URL = f"mysql+mysqlconnector://root:{MYSQL_PASSWORD}@localhost/{os.getenv('DATABASE_NAME')}"


class Base(DeclarativeBase):
    pass


class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    make: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    location: Mapped[str] = mapped_column(String(100), nullable=False)
    exterior_color: Mapped[str | None] = mapped_column(String(100))
    interior_color: Mapped[str | None] = mapped_column(String(255))
    licensing_scheme: Mapped[str | None] = mapped_column(String(255))
    transmission: Mapped[str | None] = mapped_column(String(100))
    body_type: Mapped[str | None] = mapped_column(String(100))
    air_conditioning: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    doors: Mapped[int | None] = mapped_column(Integer)
    details: Mapped[str | None] = mapped_column(Text)
    restoration: Mapped[str | None] = mapped_column(Text)

    contacts: Mapped[list["VehicleContact"]] = relationship(back_populates="vehicle", cascade="all, delete-orphan")


class VehicleContact(Base):
    __tablename__ = "vehicle_contacts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    number: Mapped[str | None] = mapped_column(String(50))

    vehicle: Mapped["Vehicle"] = relationship(back_populates="contacts")


class ToyCar(Base):
    __tablename__ = "toy_cars"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    detail: Mapped[str | None] = mapped_column(String(255))


engine = create_engine(DATABASE_URL, echo=False)


def get_engine_without_db():
    return create_engine(f"mysql+mysqlconnector://root:{MYSQL_PASSWORD}@localhost", echo=False)


def create_database():
    from sqlalchemy import text
    eng = get_engine_without_db()
    with eng.connect() as conn:
        conn.execute(text("CREATE DATABASE IF NOT EXISTS classic_car"))
        conn.commit()
    print("Database 'classic_car' created.")


def create_tables():
    Base.metadata.create_all(engine)
    print("Tables created.")


def transfer_data():
    with open(BASE_DIR / "data" / "data.json", encoding="utf-8") as f:
        vehicles = json.load(f)

    with open(BASE_DIR / "data" / "toy_car_details.json", encoding="utf-8") as f:
        toy_cars = json.load(f)

    with Session(engine) as session:
        for v in vehicles:
            vehicle = Vehicle(
                id=v["id"],
                name=v["name"],
                make=v["make"],
                model=v["model"],
                year=v["year"],
                price=v["price"],
                location=v["location"],
                exterior_color=v["exterior_color"],
                interior_color=v["interior_color"],
                licensing_scheme=v["licensing_scheme"],
                transmission=v["transmission"],
                body_type=v["body_type"],
                air_conditioning=v["air_conditioning"],
                doors=v["doors"],
                details=v["details"],
                restoration=v["restoration"],
                contacts=[
                    VehicleContact(name=c["name"], number=c["number"])
                    for c in v["contact"]
                ],
            )
            session.add(vehicle)

        for t in toy_cars:
            session.add(ToyCar(id=t["id"], name=t["name"], detail=t["detail"]))

        session.commit()

    print(f"Seeded {len(vehicles)} vehicles, {len(toy_cars)} toy cars.")


def view_data():
    with Session(engine) as session:
        vehicles = session.query(Vehicle).all()
        print(f"\n{'=' * 40}")
        print(f"VEHICLES ({len(vehicles)} rows)")
        print(f"{'=' * 40}")
        for v in vehicles:
            print(f"\n--- Vehicle ID {v.id} ---")
            for col in Vehicle.__table__.columns:
                print(f"  {col.name}: {getattr(v, col.name)}")

        contacts = session.query(VehicleContact).all()
        print(f"\n{'=' * 40}")
        print(f"VEHICLE CONTACTS ({len(contacts)} rows)")
        print(f"{'=' * 40}")
        for c in contacts:
            print(f"  {{'id': {c.id}, 'vehicle_id': {c.vehicle_id}, 'name': '{c.name}', 'number': '{c.number}'}}")

        toys = session.query(ToyCar).all()
        print(f"\n{'=' * 40}")
        print(f"TOY CARS ({len(toys)} rows)")
        print(f"{'=' * 40}")
        for t in toys:
            print(f"  {{'id': {t.id}, 'name': '{t.name}', 'detail': '{t.detail}'}}")


def main():
    # create_database()
    # create_tables()
    # transfer_data()
    view_data()


if __name__ == "__main__":
    main()
