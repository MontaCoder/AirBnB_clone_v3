#!/usr/bin/python3
""" view for Amenity objects that handles all default RESTFul API actions """

from api.v1.views import app_views
from flask import jsonify, Blueprint, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def get_amenities():
    """ Retrieves the list of all Amenity objects """
    amenities = []
    for obj in storage.all('Amenity').values():
        amenities.append(obj.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<am_id>', methods=['GET', 'DELETE'])
def get_amenity(am_id):
    """ Retrieves or Deletes a Amenity object """
    for obj in storage.all('Amenity').values():
        if obj.id == am_id:
            if request.method == 'GET':
                return jsonify(obj.to_dict())
            if request.method == 'DELETE':
                storage.delete(obj)
                storage.save()
                return jsonify({}), 200
    abort(404)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def create_amenity():
    """ Create amenity """
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')

    amenities = []
    new_amenity = Amenity(name=request.json['name'])
    storage.new(new_amenity)
    storage.save()
    amenities.append(new_amenity.to_dict())
    return jsonify(amenities[0]), 201


@app_views.route('/amenities/<am_id>', strict_slashes=False, methods=['PUT'])
def updates_amenity(am_id):
    """ Updates an Amenity object """
    amenities = storage.all("Amenity").values()
    amenity_obj = [obj.to_dict() for obj in amenities if obj.id == am_id]
    if amenity_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    amenity_obj[0]['name'] = request.json['name']
    for obj in amenities:
        if obj.id == am_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(amenity_obj[0]), 200
