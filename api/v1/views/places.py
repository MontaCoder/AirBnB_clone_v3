#!/usr/bin/python3
"""
Create a new view for Place objects
that handles all default RESTFul API actions
"""
from flask import abort
from flask import jsonify
from flask import request
from models.city import City
from models.place import Place
from models.user import User
from api.v1.views import app_views
from models import storage


@app_views.route("/cities/<city_id>/places", methods=["GET"], strict_slashes=False)
def get_places_by_city(city_id):
    """A route that returns get palces by city"""
    city = storage.get(City, city_id)
    if not city:
        return abort(404)

    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """A route that returns get place"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        return abort(404)


@app_views.route("/places/<place_id>", methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    """A route that returns delete place"""
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route("/cities/<city_id>/places", methods=["POST"], strict_slashes=False)
def create_place(city_id):
    """A route that returns create place"""
    city = storage.get(City, city_id)
    if not city:
        return abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    data = request.get_json()
    if "user_id" not in data:
        abort(400, "Missing user_id")
    if "name" not in data:
        abort(400, "Missing name")

    user = storage.get(User, data["user_id"])
    if not user:
        return abort(404)

    data["city_id"] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """A route that returns update place"""
    if place:
        if not request.get_json():
            abort(400, "Not a JSON")

        data = request.get_json()
        ignore_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(place, key, value)

        place.save()
        return jsonify(place.to_dict()), 200
    else:
        return abort(404)
