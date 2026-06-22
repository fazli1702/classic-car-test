import json
from pathlib import Path
from dotenv import load_dotenv
import os

from flask import Flask
from sqlalchemy import create_engine, text

from database.models import db, Vehicle, VehicleContact, ToyCar

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
DATABASE_URL = f"mysql+mysqlconnector://root:{MYSQL_PASSWORD}@localhost/classic_car"


def get_engine_without_db():
    return create_engine(f"mysql+mysqlconnector://root:{MYSQL_PASSWORD}@localhost", echo=False)


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    db.init_app(app)
    return app


def create_database():
    eng = get_engine_without_db()
    with eng.connect() as conn:
        conn.execute(text("CREATE DATABASE IF NOT EXISTS classic_car"))
        conn.commit()
    print("Database 'classic_car' created.")


def create_tables():
    app = create_app()
    with app.app_context():
        db.create_all()
    print("Tables created.")


def transfer_data():
    with open(BASE_DIR / "data" / "data.json", encoding="utf-8") as f:
        vehicles = json.load(f)

    with open(BASE_DIR / "data" / "toy_car_details.json", encoding="utf-8") as f:
        toy_cars = json.load(f)

    app = create_app()
    with app.app_context():
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
            db.session.add(vehicle)

        for t in toy_cars:
            db.session.add(ToyCar(id=t["id"], name=t["name"], detail=t["detail"]))

        db.session.commit()

    print(f"Seeded {len(vehicles)} vehicles, {len(toy_cars)} toy cars.")


def view_data():
    app = create_app()
    with app.app_context():
        vehicles = db.session.query(Vehicle).all()
        print(f"\n{'=' * 40}")
        print(f"VEHICLES ({len(vehicles)} rows)")
        print(f"{'=' * 40}")
        for v in vehicles:
            print(f"\n--- Vehicle ID {v.id} ---")
            for col in Vehicle.__table__.columns:
                print(f"  {col.name}: {getattr(v, col.name)}")

        contacts = db.session.query(VehicleContact).all()
        print(f"\n{'=' * 40}")
        print(f"VEHICLE CONTACTS ({len(contacts)} rows)")
        print(f"{'=' * 40}")
        for c in contacts:
            print(f"  {{'id': {c.id}, 'vehicle_id': {c.vehicle_id}, 'name': '{c.name}', 'number': '{c.number}'}}")

        toys = db.session.query(ToyCar).all()
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
