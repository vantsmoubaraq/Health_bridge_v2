#!/usr/bin/python3

"""Module populates all views"""
from flask import Flask, render_template, request, session, redirect, url_for, flash, abort
from models.patients import Patient
import models
from models.base_model import BaseModel
from models.drugs import Drug
from models.users import User
import random
from models.payments import Payment
from models.services import Service
import requests
from datetime import datetime, timedelta, timezone
import pytz
import secrets
from functools import wraps
from api.v1.auth import Auth
from werkzeug.security import generate_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.debug = True
app.secret_key = secrets.token_hex(32)
Auth = Auth()

login_manager = LoginManager(app)
login_manager.init_app(app)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
    # Load the user from the database based on user_id
    # Return the user object or None if not found
    return models.storage.search_one("User", id=user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Validate the user's credentials (e.g., check email and password against the database)
        user = models.storage.search_one("User", email=email)
        if user and user.check_password(password):
            # Login the user
            login_user(user)
            return "hello_world"
        else:
            flash('Invalid email or password')
    else:
        return render_template('login_signup.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form.get('name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        email = request.form.get('email')
        password = request.form.get('password')
        contact = request.form.get('contact')
        role = request.form.get('role')

        # Create a new User instance
        new_user = User(
            name=name,
            age=age,
            gender=gender,
            email=email,
            password=generate_password_hash(password),
            contact=contact,
            role=role
        )
        user = models.storage.search_one("User", email=email)
        if user:
            abort(403)
        new_user.save()
        # Save the new user to the database
        # Replace this with your database logic to save the user
        # Example: db.session.add(new_user); db.session.commit()

        # Log in the user after successful signup
        login_user(new_user)

        # Redirect the user to the home page or any desired page
        return render_template("patients_page.html")

    return render_template('login_signup.html')

@app.route('/logout')
@login_required
def logout():
    # Logout the user
    logout_user()
    return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    # Access the current user using `current_user` and retrieve the necessary profile information
    user = current_user
    return render_template('profile.html', user=user)

"""
@app.route('/password-update', methods=['GET', 'POST'])
@login_required
def password_update():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']

        # Validate the user's current password and update the password in the database
        user = current_user
        if user.check_password(current_password):
            user.set_password(new_password)
            db.session.commit()
            flash('Password updated successfully')
            return redirect(url_for('profile'))
        else:
            flash('Invalid current password')

    return render_template('password_update.html')
"""

@app.route("/", strict_slashes=False)
@login_required
def all_patients():
    """Populates all patients view"""
    if models.storage_env == "db":
        models.storage.save()
    else:
        models.storage.reload()
    image_urls = ["../static/images/p1.jpeg", "../static/images/p2.jpeg", "../static/images/p3.jpeg", "../static/images/p4.jpeg", "../static/images/p5.jpeg", "../static/images/p6.jpeg", "../static/images/p7.jpeg", "../static/images/p8.jpeg"]
    """random.shuffle(image_urls)
    chosen = image_urls[0]"""
    patients = sorted(list(models.storage.all("Patient").values()),
                      key=lambda a: a.created_at)
    if models.storage_env == "db":
        for patient in patients:
            random.shuffle(image_urls)
            patient.image_url = image_urls.pop(0)
            image_urls.append(patient.image_url)
    return render_template("patients_page.html", patients=patients, storage_env=models.storage_env)


@app.route("/pharmacy", strict_slashes=False)
@login_required
def pharmacy():
    """Implements pharmacy view"""
    if models.storage_env == "db":
        models.storage.save()
    else:
        models.storage.reload()
    drug_urls = ["../static/images/drug1.jpeg", "../static/images/drug2.jpeg", "../static/images/drug3.jpeg", "../static/images/drug4.jpeg", "../static/images/drug5.jpeg", "../static/images/drug6.jpeg", "../static/images/drug7.jpeg", "../static/images/drug8.jpeg"]
    drugs = sorted(list(models.storage.all("Drug").values()),
                   key=lambda x: x.name)
    if models.storage_env == "db":
        for drug in drugs:
            random.shuffle(drug_urls)
            drug.drug_img = drug_urls.pop(0)
            drug_urls.append(drug.drug_img)
    return render_template("pharmacy_page.html", drugs=drugs, storage_env=models.storage_env)

@app.route("/single/<string:patient_id>", strict_slashes=False)
@login_required
def single_patient(patient_id):
    """Handles single patient_view"""
    image_urls = ["../static/images/p1.jpeg", "../static/images/p2.jpeg", "../static/images/p3.jpeg", "../static/images/p4.jpeg", "../static/images/p5.jpeg", "../static/images/p6.jpeg", "../static/images/p7.jpeg", "../static/images/p8.jpeg"]
    if models.storage_env == "db":
        models.storage.save()
    else:
        models.storage.reload()
    random.shuffle(image_urls)
    chosen = image_urls[0]
    patient = models.storage.get("Patient", patient_id)
    return render_template("single_patient.html", patient=patient, chosen=chosen)

@app.route("/create_patient", strict_slashes=False)
def create_patient():
    """Returns patient form"""
    return render_template("patient_form.html")

@app.route("/edit_patient/<string:patient_id>", strict_slashes=False)
def edit_patient(patient_id):
    """Returns patient form"""
    patient = models.storage.get("Patient", patient_id)
    return render_template("patient_edit_form.html", patient=patient)

@app.route("/create_drug", strict_slashes=False)
def create_drug():
    """Displays drug form"""
    return render_template("drugs_form.html")

@app.route("/prescriptions/<string:patient_id>", strict_slashes=False)
def add_prescriptions(patient_id):
    """Displays prescriptions for a patient"""
    if models.storage_env == "db":
        models.storage.save()
    else:
        models.storage.reload()
    patient = models.storage.get("Patient", patient_id)
    drugs = patient.drugs
    now = datetime.now().strftime('%Y-%m-%d  %H:%M:%S')
    return render_template("prescriptions_view.html", patient=patient, drugs=drugs, now=now)

@app.route("/all_payments/<string:patient_id>", strict_slashes=False)
def all_payments(patient_id):
    """Displays payments"""
    if models.storage_env == "db":
        models.storage.save()
    else:
        models.storage.reload()
    patient = models.storage.get("Patient", patient_id)
    payments = sorted(list(models.storage.all("Payment").values()), key=lambda x: x.created_at)

    patient_payments = []
    for payment in payments:
        if payment.patient_id == patient.id:
            patient_payments.append(payment)

    return render_template("payments_view.html", patient=patient, patient_payments=patient_payments)

@app.route("/create_payment/<string:patient_id>", strict_slashes=False)
def create_payment(patient_id):
    """creates payment against patient"""
    return render_template("payment_form.html")

@app.route("/edit_payment/<string:payment_id>", strict_slashes=False)
def edit_payment(payment_id):
    """Displays payment edit form"""
    payment = models.storage.get("Payment", payment_id)
    patients = list(models.storage.all("Patient").values())
    patient = None
    for pat in patients:
        if pat.id == payment.patient_id:
            patient = models.storage.get("Patient", pat.id)
    return render_template("payment_edit_form.html", payment=payment, patient=patient)

@app.route("/single_drug/<string:drug_id>", strict_slashes=False)
def single_drug(drug_id):
    """Displays single drug"""
    if models.storage_env == "db":
        models.storage.save()
    else:
        models.storage.reload()
    drug = models.storage.get("Drug", drug_id)
    return render_template("single_drug.html", drug=drug)

@app.route("/edit_drug/<string:drug_id>", strict_slashes=False)
def edit_drug(drug_id):
    """Edits drug"""
    drug = models.storage.get("Drug", drug_id)
    return render_template("drug_edit_form.html", drug=drug)

@app.route("/search_patients", strict_slashes=False)
def search_patient():
    """Displays patients based on a query string"""
    query = request.args.get('q')
    
    patients = models.storage.search(query, "Patient")
    return render_template("patient_search.html", patients=patients)

@app.route("/search_drugs", strict_slashes=False)
def search_drug():
    """Displays drugs based on a query string"""
    query = request.args.get("q")
    drugs = models.storage.search(query, "Drug")
    return render_template("pharmacy_search.html", drugs=drugs)

@app.route("/search_prescription/<string:patient_id>", strict_slashes=False)
def search_prescriptions(patient_id):
    """Displays drugs based on a search query"""
    patient = models.storage.get("Patient", patient_id)
    query = request.args.get("q")
    drugs = models.storage.search(query, "Drug")
    return render_template("prescription_search.html", drugs=drugs)

@app.route("/appointments", strict_slashes=False)
def telemedicine():
    """Display appointments from calendly api"""
    access_token = "eyJraWQiOiIxY2UxZTEzNjE3ZGNmNzY2YjNjZWJjY2Y4ZGM1YmFmYThhNjVlNjg0MDIzZjdjMzJiZTgzNDliMjM4MDEzNWI0IiwidHlwIjoiUEFUIiwiYWxnIjoiRVMyNTYifQ.eyJpc3MiOiJodHRwczovL2F1dGguY2FsZW5kbHkuY29tIiwiaWF0IjoxNjgwMDA2NjMzLCJqdGkiOiI5ZWM0YTU2Yy02MGY3LTRhZTYtYTdhNy1hNThiODQyNzM0ODEiLCJ1c2VyX3V1aWQiOiJhMzk0ZjgxMS1mNjdlLTQyYTMtODcyYS1iYzM4MzU4NzM1YzAifQ.4Iz5ISUjOf0oy5J6HjHTU1kv-sTG2ff2A9w_R6-aGGjcDvNx5qj3BxxRu8WC-055bXTBsAA5QkQAp0uOXNDlmg"
    endpoint = "https://api.calendly.com/scheduled_events"
    
    now = datetime.utcnow()
    min_start_time = now - timedelta(days=7)
    min_start_time_utc = min_start_time.replace(tzinfo=timezone.utc)
    min_start_time = min_start_time_utc.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    params = {"user": "https://api.calendly.com/users/a394f811-f67e-42a3-872a-bc38358735c0", "min_start_time": min_start_time}

    response = requests.get(endpoint, headers=headers, params=params)
    response = response.json()
    
    all_events = events(response)
    all_invitees = invitees(all_events, headers)

    for event in all_events:
        for invitee in all_invitees:
            if event["uri"] in invitee:
                event.update(invitee[event["uri"]])
    return render_template("appointments.html", all_events=all_events)


@app.route("/log", strict_slashes=False)
def log():
    """renders login page"""
    return render_template("login_signup.html")

@app.route("/signup")
def sign_up():
    """renders login page"""
    return render_template("login_signup.html")

@app.route("/services", strict_slashes=False)
def services():
    """Displays all services"""
    if models.storage_env == "db":
        models.storage.save()
    else:
        models.storage.reload()
    services = sorted(list(models.storage.all("Service").values()), key=lambda x: x.name)
    return render_template("services.html", services=services, storage_env=models.storage_env)

@app.route("/edit_service/<string:service_id>", strict_slashes=False)
def edit_service(service_id):
    """Displays service edit form"""
    service = models.storage.get("Service", service_id)
    return render_template("service_edit_form.html", service=service)

@app.route("/delete_service/<string:service_id>", strict_slashes=False)
def delete_service(service_id):
    """Deletes a service"""
    service = models.storage.get("Service", service_id)
    if service:
        models.storage.delete(service)
        models.storage.save()
    return redirect("/services")

@app.route("/create_service", strict_slashes=False)
def create_service():
    """Displays service creation form"""
    return render_template("service_create_form.html")

@app.route("/service/<string:service_id>", strict_slashes=False)
def single_service(service_id):
    """Displays a single service"""
    if models.storage_env == "db":
        models.storage.save()
    else:
        models.storage.reload()
    service = models.storage.get("Service", service_id)
    return render_template("single_service.html", service=service)

@app.route("/search_services", strict_slashes=False)
def search_service():
    """Displays drugs based on a query string"""
    query = request.args.get("q")
    services = models.storage.search(query, "Service")
    return render_template("service_search.html", services=services)


def events(response):
    """returns all events in last 7 days"""
    event_details = []

    for event in response["collection"]:
        uri = event["uri"]
        uri = uri.split("/")[4]
        location = event["location"].get("join_url", None)
        name = event["name"]
        start_time = event["start_time"]
        start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.%fZ')
        start_time = pytz.utc.localize(start_time).astimezone(pytz.timezone('AFRICA/Nairobi'))
        start_time = start_time.strftime('%Y-%m-%d | %H:%M:%S')
        status = event["status"]
        event_details.append({"uri": uri, "location": location, "name": name, "start_time": start_time, "status": status})
    return(event_details)

def invitees(all_events, headers):
    """Returns invitee details"""
    invitee_ids = []
    for event in all_events:
        invitee_ids.append(event["uri"])

    invitee_details = []
    for invitee_id in invitee_ids:
        invitee_url = f"https://api.calendly.com/scheduled_events/{invitee_id}/invitees"
        r = requests.get(invitee_url, headers=headers)
        r = r.json()
        if "collection" in r:
            user_name = r.get("collection", None)[0]["name"]
            user_email = r.get("collection", None)[0]["email"]
            invitee_details.append({invitee_id: {"user_name": user_name, "user_email": user_email}})
    return(invitee_details)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
