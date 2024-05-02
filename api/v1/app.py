#!/usr/bin/python3
"""Create a flask app that starts an API"""
from os import getenv
from flask import Flask
from flask import jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
# Create a Flask application instance
app = Flask(__name__)

CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})

# Register the blueprint app_views to the Flask instance app
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_engine(exception):
    """A route that returns teardown engine"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """A route that returns not found"""
    response = {"error": "Not found"}
    return jsonify(response), 404


# Run the Flask server
if __name__ == "__main__":
    HOST = getenv("HBNB_API_HOST", "0.0.0.0")
    PORT = int(getenv("HBNB_API_PORT", 5000))
    app.run(host=HOST, port=PORT, threaded=True)
