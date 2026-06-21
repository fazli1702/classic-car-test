import json
import os
import re
from datetime import date
from pathlib import Path
from dotenv import load_dotenv

from flask import Flask, render_template, abort, request, flash, redirect, url_for
from flask_mail import Mail, Message

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__,
            template_folder=str(BASE_DIR / 'templates'),
            static_folder=str(BASE_DIR / 'static'))

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
# --- Flask-Mail Configuration ---
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Replace with your provider
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")  # Your email address
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")    # Your App Password (not your login password)
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_USERNAME")

mail = Mail(app)

with open(BASE_DIR / 'data' / 'data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

with open(BASE_DIR / 'data' / 'toy_car_details.json', 'r', encoding='utf-8') as file:
    TOY_CAR_DETAILS = json.load(file)

for i, vehicle in enumerate(data):
    folder = str(i + 1)
    img_dir = BASE_DIR / 'static' / 'images' / 'car_images' / folder
    files = sorted(
        [f for f in os.listdir(img_dir) if f.endswith('.jpg')],
        key=lambda f: int(os.path.splitext(f)[0])
    )
    image_paths = [f'/static/images/car_images/{folder}/{f}' for f in files]
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


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message_body = request.form.get('message', '').strip()

        msg = Message(
            subject=f"Enquiry: {subject}",
            recipients=[app.config['MAIL_USERNAME']],
            reply_to=email,
            body=f"Name: {name}\nEmail: {email}\n\n{message_body}"
        )
        try:
            mail.send(msg)
            flash('Your enquiry has been sent successfully. We will get back to you shortly.', 'success')
        except Exception:
            flash('Something went wrong. Please try again later.', 'error')
        return redirect(url_for('contact'))

    return render_template("contact.html")


@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == '__main__':
    app.run(debug=True)