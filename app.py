import os
from datetime import date
from pathlib import Path
from dotenv import load_dotenv

from flask import Flask, render_template, abort, request, flash, redirect, url_for
from flask_mail import Mail, Message

from database.models import db, Vehicle, ToyCar

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__,
            template_folder=str(BASE_DIR / 'templates'),
            static_folder=str(BASE_DIR / 'static'))

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
app.config['SQLALCHEMY_DATABASE_URI'] = f"{os.getenv("MYSQL_URL")}"

# --- Flask-Mail Configuration ---
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_USERNAME")

db.init_app(app)
mail = Mail(app)

app.jinja_env.filters['currency'] = lambda v: f"S${v:,}"

def enrich_vehicle(vehicle):
    folder = str(vehicle.id)
    img_dir = BASE_DIR / 'static' / 'images' / 'car_images' / folder
    files = sorted(
        [f for f in os.listdir(img_dir) if f.endswith('.jpg')],
        key=lambda f: int(os.path.splitext(f)[0])
    )
    image_paths = [f'/static/images/car_images/{folder}/{f}' for f in files]
    vehicle.src = image_paths[0] if image_paths else ''
    vehicle.images = image_paths
    vehicle.price_numeric = vehicle.price
    vehicle.contact = vehicle.contacts
    return vehicle


@app.route('/')
def home():
    vehicles = Vehicle.query.limit(4).all()
    vehicle_details = [enrich_vehicle(v) for v in vehicles]
    return render_template("index.html", vehicle_details=vehicle_details)


@app.route('/buy')
def buy():
    vehicles = Vehicle.query.all()
    vehicle_details = [enrich_vehicle(v) for v in vehicles]
    makes = sorted({v.make for v in vehicle_details})
    models = sorted({v.model for v in vehicle_details})
    return render_template("buy.html", vehicle_details=vehicle_details, makes=makes, models=models, current_year=date.today().year)


@app.route('/details/<int:vehicle_id>')
def details(vehicle_id):
    vehicle = db.session.get(Vehicle, vehicle_id)
    if vehicle is None:
        abort(404)
    enrich_vehicle(vehicle)
    return render_template("details.html", vehicle=vehicle)


@app.route('/sell')
def sell():
    return render_template("sell.html")


@app.route('/toys')
def toys():
    toy_cars = ToyCar.query.all()
    return render_template("toys.html", toy_cars=toy_cars)


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
