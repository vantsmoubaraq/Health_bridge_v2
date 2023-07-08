#!/usr/bin/python3

"""Module is entry point to API"""

from flask import Flask, jsonify, make_response
from api.v1.views import ui
from flask_cors import CORS
from models import storage
from flasgger import Swagger
from flasgger.utils import swag_from
import secrets

app = Flask(__name__)
app.register_blueprint(ui)
app.debug = True
CORS(app)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.secret_key = secrets.token_hex(32)

"""
@app.teardown_appcontext
def close(error):
    close transaction
    storage.close()
"""
@app.errorhandler(404)
def not_found(error):
    """Handles 404 error"""
    return make_response(jsonify({"error": "Not found"}), 404)

app.config['SWAGGER'] = {
    'title': 'HealthBridge API',
    'uiversion': 1
}
swagger = Swagger(app)

if __name__ == "__main__":
    """Run application"""
    app.run(host="0.0.0.0", port="5001", threaded=True)
