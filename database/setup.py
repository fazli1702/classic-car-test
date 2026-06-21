import json
from pathlib import Path
from dotenv import load_dotenv
import os

import mysql.connector

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

def get_connection(database=None):
    config = {
        "host": "localhost",
        "user": "root",
        "password": os.getenv("MYSQL_PASSWORD")
    }
    if database:
        config["database"] = database
    return mysql.connector.connect(**config)


def create_database():
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS classic_car")
    cursor.close()
    db.close()
    print("Database 'classic_car' created.")


def create_tables():
    db = get_connection("classic_car")
    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            make VARCHAR(100) NOT NULL,
            model VARCHAR(100) NOT NULL,
            year YEAR NOT NULL,
            price INT NOT NULL,
            location VARCHAR(100) NOT NULL,
            exterior_color VARCHAR(100),
            interior_color VARCHAR(255),
            licensing_scheme VARCHAR(255),
            transmission VARCHAR(100),
            body_type VARCHAR(100),
            air_conditioning BOOLEAN NOT NULL DEFAULT FALSE,
            doors INT,
            details TEXT,
            restoration TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicle_contacts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            vehicle_id INT NOT NULL,
            name VARCHAR(255) NOT NULL,
            number VARCHAR(50),
            FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS toy_cars (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            detail VARCHAR(255)
        )
    """)

    cursor.close()
    db.close()
    print("Tables created.")


def transfer_data():
    db = get_connection("classic_car")
    cursor = db.cursor()

    with open(BASE_DIR / "data" / "data.json", encoding="utf-8") as f:
        vehicles = json.load(f)

    with open(BASE_DIR / "data" / "toy_car_details.json", encoding="utf-8") as f:
        toy_cars = json.load(f)

    for v in vehicles:
        cursor.execute("""
            INSERT INTO vehicles (id, name, make, model, year, price, location,
                exterior_color, interior_color, licensing_scheme, transmission,
                body_type, air_conditioning, doors, details, restoration)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            v["id"], v["name"], v["make"], v["model"], v["year"], v["price"],
            v["location"], v["exterior_color"], v["interior_color"],
            v["licensing_scheme"], v["transmission"], v["body_type"],
            v["air_conditioning"], v["doors"], v["details"], v["restoration"]
        ))

        for contact in v["contact"]:
            cursor.execute("""
                INSERT INTO vehicle_contacts (vehicle_id, name, number)
                VALUES (%s, %s, %s)
            """, (v["id"], contact["name"], contact["number"]))

    for t in toy_cars:
        cursor.execute("""
            INSERT INTO toy_cars (id, name, detail)
            VALUES (%s, %s, %s)
        """, (t["id"], t["name"], t["detail"]))

    db.commit()
    cursor.close()
    db.close()
    print(f"Seeded {len(vehicles)} vehicles, {len(toy_cars)} toy cars.")


def view_data():
    db = get_connection("classic_car")
    cursor = db.cursor()

    cursor.execute("SELECT * FROM vehicles")
    vehicles = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    print(f"\n{'=' * 40}")
    print(f"VEHICLES ({len(vehicles)} rows)")
    print(f"{'=' * 40}")
    for row in vehicles:
        print(f"\n--- Vehicle ID {row[0]} ---")
        for col, val in zip(columns, row):
            print(f"  {col}: {val}")

    cursor.execute("SELECT * FROM vehicle_contacts")
    contacts = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    print(f"\n{'=' * 40}")
    print(f"VEHICLE CONTACTS ({len(contacts)} rows)")
    print(f"{'=' * 40}")
    for row in contacts:
        print(f"  {dict(zip(columns, row))}")

    cursor.execute("SELECT * FROM toy_cars")
    toys = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    print(f"\n{'=' * 40}")
    print(f"TOY CARS ({len(toys)} rows)")
    print(f"{'=' * 40}")
    for row in toys:
        print(f"  {dict(zip(columns, row))}")

    cursor.close()
    db.close()


def main():
    # create_database()
    # create_tables()
    # transfer_data()
    view_data()


if __name__ == "__main__":
    main()
