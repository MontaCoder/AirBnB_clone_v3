#!/usr/bin/python3
""" Places view """
from api.v1.views import app_views
from flask import jsonify, Blueprint, abort, request
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', strict_slashes=False, methods=[
    'GET'])
def all_places(city_id):
    """ Retrieves the list of objects of a specific city"""

    all_places = []
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    for place in storage.all("Place").values():
        if city_id == place.city_id:
            all_places.append(place.to_dict())
    return jsonify(all_places)


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE'])
def get_place(place_id):
    """ Retrieves a place object """
    for obj in storage.all("Place").values():
        if obj.id == place_id:
            if request.method == 'GET':
                return jsonify(obj.to_dict())
            if request.method == 'DELETE':
                storage.delete(obj)
                storage.save()
                return jsonify({}), 200
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def post_new_data(city_id):
    """ add new places to a specific city """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    if "user_id" not in request.get_json():
        abort(400, "Missing user_id")

    user = storage.get('User', request.get_json()['user_id'])
    if user is None:
        abort(404)

    if "name" not in request.get_json():
        abort(400, "Missing name")
    request.get_json()['city_id'] = city_id
    place = Place(**request.get_json())
    place.save()
    return (jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place_id(place_id):
    """ update the place with its id """
    if not request.get_json():
        abort(400, "Not a JSON")

    ignored_keys = ['id', 'city_id', 'created_at', 'updated_at', 'user_id']
    for place in storage.all("Place").values():
        if place.id == place_id:
            for key, value in request.get_json().items():
                if key not in ignored_keys:
                    setattr(place, key, value)
            place.save()
            return jsonify(place.to_dict())
    abort(404)
