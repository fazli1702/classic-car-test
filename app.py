import json
import os
import re
from datetime import date
from pathlib import Path

from flask import Flask, render_template, abort

BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__,
            template_folder=str(BASE_DIR / 'templates'),
            static_folder=str(BASE_DIR / 'static'))


with open(BASE_DIR / 'data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

with open(BASE_DIR / 'toy_car_details.json', 'r', encoding='utf-8') as file:
    TOY_CAR_DETAILS = json.load(file)

for i, vehicle in enumerate(data):
    folder = str(i + 1)
    img_dir = BASE_DIR / 'static' / 'images' / folder
    files = sorted(
        [f for f in os.listdir(img_dir) if f.endswith('.jpg')],
        key=lambda f: int(os.path.splitext(f)[0])
    )
    image_paths = [f'/static/images/{folder}/{f}' for f in files]
    vehicle['id'] = i + 1
    vehicle['src'] = image_paths[0] if image_paths else ''
    vehicle['images'] = image_paths
    digits = re.sub(r'[^\d]', '', vehicle.get('price', '').split('.')[0])
    vehicle['price_numeric'] = int(digits) if digits else 0

VEHICLE_DETAILS = data


def format_to_currency(amount: int) -> str:
    """Converts an integer to a string in Singapore Dollar (S$) currency format."""
    return f"S${amount:,}"


def get_formatted_vehicles():
    """Returns the vehicle list with prices formatted as Singapore Dollars."""
    # return [
    #     {**vehicle, "price": format_to_currency(vehicle["price"])}
    #     for vehicle in VEHICLE_DETAILS
    # ]
    global VEHICLE_DETAILS
    vehicle_details = VEHICLE_DETAILS
    return vehicle_details



@app.route('/')
def home():
    # Homepage only teases a handful of vehicles
    vehicle_details = get_formatted_vehicles()[:4]
    return render_template("index.html", vehicle_details=vehicle_details)


@app.route('/buy')
def buy():
    vehicle_details = get_formatted_vehicles()
    makes = sorted({vehicle["make"] for vehicle in VEHICLE_DETAILS})
    models = sorted({vehicle["model"] for vehicle in VEHICLE_DETAILS})
    return render_template("buy.html", vehicle_details=vehicle_details, makes=makes, models=models, current_year=date.today().year)

@app.route('/details/<int:vehicle_id>')
def details(vehicle_id):
    vehicle = next((v for v in VEHICLE_DETAILS if v["id"] == vehicle_id), None)
    if vehicle is None:
        abort(404)
    return render_template("details.html", vehicle=vehicle)


@app.route('/sell')
def sell():
    return render_template("sell.html")


@app.route('/toys')
def toys():
    return render_template("toys.html", toy_cars=TOY_CAR_DETAILS)


@app.route('/services')
def services():
    return render_template("services.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == '__main__':
    app.run(debug=True)