import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Text, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class Vehicle(db.Model):
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


class VehicleContact(db.Model):
    __tablename__ = "vehicle_contacts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    number: Mapped[str | None] = mapped_column(String(50))

    vehicle: Mapped["Vehicle"] = relationship(back_populates="contacts")


class ToyCar(db.Model):
    __tablename__ = "toy_cars"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    detail: Mapped[str | None] = mapped_column(String(255))
