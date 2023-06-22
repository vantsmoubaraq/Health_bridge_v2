![The logo](https://pbs.twimg.com/media/Fq3FPVVXoAADhSL?format=jpg&name=900x900)
  
*The primary objective of this project was to develop a user-friendly and comprehensive Hospital Management System software solution that can address the needs of hospitals and improve their operations. The solution  covers all aspects of hospital management, including patient information management, appointment scheduling, telemedicine, inventory management, medical billing, and electronic health records.* 
  

  ![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

![HealthBridge Patients Management Page](https://github.com/vantsmoubaraq/Health_bridge_v1/blob/master/landing_page/images/patients%20(2).png?raw=true)
<p align="right">
<sub>(Preview)</sub>
</p>
  

* 🖥️ Checkout our application @ [<span style="color: green;">HealthBridge</span>](http://healthbridge.techaccess.tech/)  
* 🌍 Read our [Blog](https://www.linkedin.com/pulse/health-bridge-hms-fabrizia-renish%3FtrackingId=utzLEGe%252FQJGFRQvYe4cW%252Bw%253D%253D/?trackingId=utzLEGe%2FQJGFRQvYe4cW%2Bw%3D%3D)  
* ⚡ Author: **Melvin Renish Okago**, FrontEnd Engineer, Nairobi Kenya |     [![Linkedin](https://img.shields.io/badge/LinkedIn-+22K-blue?style=social&logo=linkedin)](https://www.linkedin.com/in/fabrizia-renish-993498246/)
* ⚡ Author: **Mubarak Wantimba**, Backend Engineer, Kampala Uganda |     [![Linkedin](https://img.shields.io/badge/LinkedIn-+22K-blue?style=social&logo=linkedin)](https://www.linkedin.com/in/mubarak-wantimba-3025a820a/)
* 🤝 Contact us @ healthbridgehms@gmail.com, fabriziarenish@gmail.com, vantsmoubaraq@gmail.com
* 📌 Watch our project <a href="https://www.youtube.com/watch?v=e8JKxWIfYCo">presentation</a>
  

## ⚙️ Installation

1.  Clone this repository: `git clone "https://github.com/vantsmoubaraq/Health_bridge_v1.git"`
2.  Access HealthBridge directory: `cd Health_bridge_v1`
3.  Run the flask webserver: `python3 -m web_flask.app` Please Ensure that flask is installed on your machine
4.  Run the flask API: `python3 -m api.v1.app`
  
  
```bash git python3
$ git clone https://github.com/vantsmoubaraq/Health_bridge_v1.git

$ cd Health_bridge_v1

$ python3 -m web_flask.app

$ python3 -m api.v1.app
```

## 💾 Usage
- Open your web browser and navigate to http://localhost:5000
- Enjoy

![HealthBridge Patients Management Page](https://github.com/vantsmoubaraq/Health_bridge_v1/blob/master/landing_page/images/Screenshot%20(158).png?raw=true)

### 📖 Key Features
  
|  Feature                  | 🔰 Availability  |
| -------------------------- | :----------------: |
| Patient Management           |         ✔️         |
| Pharmacy           |         ✔️         |
| Inventory Management             |         ✔️         |
| Billing       |         ✔️         |
| Prescriptions |         ✔️         |
| Telemedicine  |         ✔️         |
| Appointments   |         ✔️         |
  

### 🔔 What Inspired Health Bridge?

* Observing a heavily pregnant family member struggle with acquiring an exercise record book.

* Un-structured and unsustainable medical record keeping process.

* Un-attended to opportunity to  analyze patient records and data

### 📝 Core algorithm
```python
#!/usr/bin/python3

"""Module implements patients api"""

from flask import Flask, abort, jsonify, make_response, request
from models import storage, storage_env
from models.patients import Patient
from api.v1.views import ui
from models.base_model import BaseModel


@ui.route("/patients", methods=["GET", "POST"])
@ui.route("/patients/<string:patient_id>", methods=["GET", "PUT", "DELETE"])
def patients(patient_id=None):
    """Handles all default RESTful API actions for patient object"""
    if patient_id:
        patient = storage.get("Patient", patient_id)
        if not patient:
            abort(404)
            return

    if request.method == "GET":
        if patient_id:
            return jsonify(patient.to_dict())
        all_patients = [obj.to_dict() for obj in
                        storage.all("Patient").values()]
        return jsonify(all_patients)

    elif request.method == "POST":
        if request.get_json() is None:
            return jsonify({"message": "Not valid json"})
        elif "name" not in request.get_json():
            return jsonify({"message": "name must be specified"})
        elif "gender" not in request.get_json():
            return jsonify({"message": "gender must be specified"})

        attr = request.get_json()
        if attr["contact"] == "None" or attr["contact"] == "":
            del attr["contact"]
        if attr["age"]  == "None" or attr["age"] == "" or attr["age"] == 0:
            del attr["age"]
        obj = Patient(**attr)
        obj.save()
        pt = storage.get("Patient", obj.id)
        return make_response(jsonify(pt.to_dict()), 201)

    elif request.method == "PUT":
        if request.get_json() is None:
            return jsonify({"message": "Not valid json"})
        attr = request.get_json()
        if attr["contact"] == "None" or attr["contact"] == "":
            del attr["contact"]
        if attr["age"] == "None" or attr["age"] == "" or attr["age"] == 0:
            del attr["age"]
        for key, value in attr.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(patient, key, value)
        patient.save()
        pt = storage.get("Patient", patient.id)
        return make_response(jsonify(pt.to_dict()), 200)

    elif request.method == "DELETE":
        patient.delete()
        storage.save()
        return (jsonify({}))

```

## ✍️ Contributing  
We welcome contributions to our project! To contribute, follow these steps:  
  
* Fork the repository on GitHub.  
* Clone your fork to your local machine using git clone `https://github.com/your-username/Health_bridge_v1.git`.  
* Create a new branch for your changes using `git checkout -b my-branch-name`.  
* Make your changes and commit them with a descriptive commit message.  
* Push your changes to your fork using `git push origin my-branch-name`.  
* Create a pull request on GitHub to merge your changes into the main repository.  
  
  ![HealthBridge Patients Management Page](https://github.com/vantsmoubaraq/Health_bridge_v1/blob/master/landing_page/images/pharmacy.png?raw=true)


## ☁️ Related Projects  
Here are some related projects that you might find useful:  
  
[HOSPITAL HUB, ](https://github.com/Dharren09/THE_HOSPITAL_HUB_v1)  By Dharren Makoha: Hospital Management Solution
  

## ⭐️ License  
*This project is licensed under the HealthBridge License.* 
  
*You are free to use, modify, and distribute this software for any purpose, commercial or non-commercial. However, please note that we are not liable for any consequences resulting from the use of this software, and we provide no warranty or support for its use.* 