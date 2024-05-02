#!/usr/bin/python3
"""
Create a new view for the link between Place objects and Amenity objects
that handles all default RESTFul API actions
"""
from flask import jsonify
from flask import abort
from flask import request
from models.place import Place
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views


@app_views.route("/places/<place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """A route that returns get place amenities"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    return jsonify([amenity.to_dict() for amneity in place.amenities])


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """A route that returns delete place amenity"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None or amenity not in place.amenities:
        abort(404)

    place.amenities.remove(amenity)
    storage.save()

    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"],
                 strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """A route that returns link place amenity"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200

    place.amenities.append(amenity)
    storage.save()

    return jsonify(amenity.to_dict()), 201
