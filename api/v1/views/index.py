#!/usr/bin/python3
"""Create a flask app that starts an API"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


# Create a route /status on the object app_views that returns JSON
@app_views.route("/status")
def api_status():
    """A route that returns status OK"""
    response = {"status": "OK"}
    return jsonify(response)


@app_views.route("/stats")
def get_stats():
    """A route that returns status OK"""
    stats = {
            "amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User"),
    }
    return jsonify(stats)
