#!/usr/bin/python3

"""Module populates all views"""
from flask import Flask, render_template, request, session, redirect, url_for, flash, abort, jsonify
from models.patients import Patient
import models
from models.base_model import BaseModel
from models.drugs import Drug
from models.users import User
import random
from models.payments import Payment
from models.services import Service
from models.messages import Message
from flask_mail import Mail, Message
import requests
from datetime import datetime, timedelta, timezone
from itsdangerous import URLSafeTimedSerializer
from werkzeug.datastructures import MultiDict
import pytz
import secrets
from functools import wraps
from flask_socketio import SocketIO, send
from api.v1.auth import Auth
from werkzeug.security import generate_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.debug = True
app.secret_key = secrets.token_hex(32)
app.config['SECRET_KEY'] = secrets.token_hex(32)
socketio = SocketIO(app, cors_allowed_origins="*")
Auth = Auth()
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'vantsmoubaraq@gmail.com'
app.config['MAIL_PASSWORD'] = 'okbovhcmqztoxeja'
app.config['MAIL_DEFAULT_SENDER'] = 'vantsmoubaraq@gmail.com'

login_manager = LoginManager(app)
login_manager.init_app(app)
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
mail = Mail(app)

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
        models.storage.save()
        email = request.form['email']
        password = request.form['password']

        # Validate the user's credentials (e.g., check email and password against the database)
        user = models.storage.search_one("User", email=email)
        if user and user.check_password(password):
            # Login the user
            login_user(user)
            return redirect(url_for('all_patients'))
        else:
            flash('Invalid email or password')
            return redirect(url_for('login'))
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


@app.route('/password-update', methods=['GET', 'POST'])
@login_required
def password_update():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']

        # Validate the user's current password and update the password in the database
        user = current_user
        if user.check_password(current_password):
            user.password = generate_password_hash(new_password)
            user.save()
            flash('Password updated successfully')
            return redirect(url_for('profile'))
        else:
            flash('Invalid current password')
    return render_template("update_password.html")

# Generate a token
def generate_token(user_id):
    token = serializer.dumps(user_id)
    return token

#send reset email
def send_password_reset_email(user, token):
    reset_link = url_for('passwd', token=token, _external=True)
    subject = 'Password Reset Request'
    body = f'Hello {user.name}, To reset your password, please click the following link: {reset_link}'
    email = Message(subject, recipients=[user.email], body=body)
    mail.send(email)


@app.route("/reset_password_token", methods=["GET", "POST"])
def reset():
    """Resets password"""
    if request.method == "POST":
        email = request.form["email"]
        user = models.storage.search_one("User", email=email)
        token = generate_token(user.id)
        user.reset_token = token
        user.save()
        send_password_reset_email(user, token)
        return render_template("forgot_passw.html")
    else:
        return render_template("forgot_passw.html")

@app.route("/reset_password", methods=["GET", "POST"])
def passwd():
    """resets forgetten password"""
    if request.method == 'POST':
        token = request.args.get("token")
        user = models.storage.search_one("User", reset_token=token)
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        if new_password == confirm_password:
            user.password = generate_password_hash(new_password)
            user.save()
        return jsonify({"password": new_password})
    return render_template('reset_passw.html')
   

@app.route('/chat')
@login_required
def index():
    name = current_user.name
    return render_template('messaging.html', name=name)

@socketio.on('message')
def handle_message(data):
    print('Received message: ' + data)
    if data != "I\'m connected!":
        #new_message = Message(content=data, sender=name)
        #new_message.save()
        send(data, broadcast=True)
    #socketio.emit('message', data, broadcast=True)

"""@socketio.on('connect')
def on_connect():
    all_messages = list(models.storage.all("Message").values())
    current_messages = []
    for message in all_messages:
        if message.sender == current_user.name:
            current_messages.append(message)

    # Convert messages to a suitable format if needed
    # Emit the message history to the connected client
    send(current_messages)"""


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
@login_required
def add_prescriptions(patient_id):
    """Displays prescriptions for a patient"""
    if models.storage_env == "db":
        models.storage.save()
    else:
        models.storage.reload()
    patient = models.storage.get("Patient", patient_id)
    prescriptions = sorted(models.storage.search_with_patient_id("Prescription", patient_id), key=lambda x: x.created_at, reverse=True)
    now = datetime.now().strftime('%Y-%m-%d  %H:%M:%S')
    user = current_user
    return render_template("prescriptions_view.html", patient=patient, prescriptions=prescriptions, now=now, user=user)

@app.route("/single_prescription/<string:prescription_id>")
@login_required
def display_prescription(prescription_id):
    """Shows single prescription"""
    models.storage.save()
    prescription = models.storage.get("Prescription", prescription_id)
    now = datetime.now().strftime('%Y-%m-%d  %H:%M:%S')
    user = current_user
    patient_id = prescription.patient_id
    patient = models.storage.get("Patient", patient_id)
    prescribed_drugs =sorted(models.storage.search_with_prescription_id("Prescribed_drug", prescription_id), key=lambda x: x.created_at, reverse=True)
    for drug in prescribed_drugs:
        actual_drug = models.storage.get("Drug", drug.drug_id)
        drug.drug_name = actual_drug.name
    return render_template("prescription_display.html", prescription=prescription, patient=patient, now=now, user=user, prescribed_drugs=prescribed_drugs)

@app.route("/invoices/<string:patient_id>", strict_slashes=False)
def show_invoices(patient_id):
    """Displays prescriptions for a patient"""
    if models.storage_env == "db":
        models.storage.save()
    else:
        models.storage.reload()
    patient = models.storage.get("Patient", patient_id)
    drugs = patient.drugs
    invoices = sorted(models.storage.search_with_patient_id("Invoice", patient_id), key=lambda x: x.created_at, reverse=True)
    total_amount = 0
    invoice_status = None
    for invoice in invoices:
        prescription_id = invoice.prescription_id
        prescribed_drugs =sorted(models.storage.search_with_prescription_id("Prescribed_drug", prescription_id), key=lambda x: x.created_at, reverse=True)
        total_amount = 0
        for drug in prescribed_drugs:
            actual_drug = models.storage.get("Drug", drug.drug_id)
            total_amount += actual_drug.price
        invoice.total_amount = total_amount
        payment = models.storage.search_one("Payment", invoice_id=invoice.id)
        if payment is None:
            invoice.paid = 0
        else:
            invoice.paid = payment.paid
        if invoice.paid < total_amount:
            invoice.status = "Open"
        else:
            invoice.status = "Paid"
        invoice_status = invoice.status
    
    return render_template("invoices.html", patient=patient, drugs=drugs, invoices=invoices, invoice_status=invoice_status)

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

@app.route("/single_invoice/<string:invoice_id>", strict_slashes=False)
@login_required
def single_invoice(invoice_id):
    """shows single invoice"""
    if not invoice_id:
        abort(404)
    invoice = models.storage.get("Invoice", invoice_id)
    patient_id = invoice.patient_id
    patient = models.storage.get("Patient", patient_id)
    user = current_user
    prescription_id = invoice.prescription_id
    if not invoice:
        abort(404)
    return render_template("customer_invoices.html", invoice=invoice, patient=patient, user=user)

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
@login_required
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
@login_required
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

<<<<<<< HEAD
@app.route("/procurements", methods=["GET"])
def get_procurements():
    """Displays all procurements"""
    if models.storage_env == "db":
        models.storage.save()
    else:
        models.storage.reload()
    procurements = sorted(list(models.storage.all("Procurement").values()),
                          key=lambda p: p.created_at)
    return render_template("procurements.html", procurements=procurements)

=======
@app.route("/prescriptions_page/<string:patient_id>", strict_slashes=False)
@login_required
def prescribe(patient_id):
    models.storage.save()
    if not patient_id:
        abort(404)
    patient = models.storage.get("Patient", patient_id)
    if not patient:
        abort(404)
    user = current_user
    drugs = list(models.storage.all("Drug").values())
    prescription = sorted(list(models.storage.all("Prescription").values()), key=lambda x: x.created_at)[-1]
    return render_template("patients_prescriptions.html", patient=patient, user=user, drugs=drugs, prescription=prescription)

@app.route("/prescriptions_edit/<string:prescription_id>", strict_slashes=False)
@login_required
def edit_prescription(prescription_id):
    """Edits prescriptions"""
    if not prescription_id:
        abort(404)
    prescription = models.storage.get("Prescription", prescription_id)
    if not prescription:
        abort(404)
    drugs = list(models.storage.all("Drug").values())
    user = current_user
    patient_id = prescription.patient_id
    patient = models.storage.get("Patient", patient_id)
    prescribed_drugs =sorted(models.storage.search_with_prescription_id("Prescribed_drug", prescription_id), key=lambda x: x.created_at, reverse=True)
    for drug in prescribed_drugs:
        actual_drug = models.storage.get("Drug", drug.drug_id)
        drug.drug_name = actual_drug.name
    return render_template("prescription_edit.html", patient=patient, user=user, drugs=drugs, prescription=prescription, prescribed_drugs=prescribed_drugs)
    
    
>>>>>>> a67c27bf4b34b060782c6463bece79780dab4cbb

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
    socketio.run(app, host='0.0.0.0', port="5000")
