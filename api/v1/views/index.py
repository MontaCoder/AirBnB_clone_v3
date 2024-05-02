#!/usr/bin/python3
"""
status route
"""
from api.v1.views import app_views
from flask import jsonify, Blueprint
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """ return status """
    state = {
        "status": "OK"
    }
    return jsonify(state)


@app_views.route('/stats', strict_slashes=False)
def stats():
    "Endpoint that retrieves the number of each objects by type"
    classes = {
        "amenities": storage.count('Amenity'),
        "cities": storage.count('City'),
        "places": storage.count('Place'),
        "reviews": storage.count('Review'),
        "states": storage.count('State'),
        "users": storage.count('User')
        }
    return jsonify(classes)
