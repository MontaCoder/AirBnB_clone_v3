#!/usr/bin/python3

"""
new view for City objects that handles
all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, Blueprint, abort, request
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities_state(state_id):
    """ get cities of specific state """
    states = storage.all('State').values()
    flag = 0
    for state in states:
        if state.id == state_id:
            flag = 1
    if flag == 0:
        abort(404)
    cities_list = []
    cities = storage.all('City').values()
    for city in cities:
        if city.state_id == state_id:
            cities_list.append(city.to_dict())
    return (jsonify(cities_list))


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_cities_id(city_id):
    """ get city with its id """
    cities = storage.all('City').values()
    for city in cities:
        if city.id == city_id:
            return (jsonify(city.to_dict()))
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city_id(city_id):
    """ delete city with its id """
    cities = storage.all('City').values()
    for city in cities:
        if city.id == city_id:
            storage.delete(city)
            storage.save()
            return jsonify({})
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
@app_views.route('/states/<state_id>/cities/', methods=['POST'])
def add_cities_state(state_id):
    """ add cities of a specific state """
    states = storage.all('State').values()
    flag = 0
    for state in states:
        if state.id == state_id:
            flag = 1
    if flag == 0:
        abort(404)

    if not request.json:
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    data = request.get_json()
    data['state_id'] = state_id
    new_city = City(**data)
    new_city.save()
    return (jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city_id(city_id):
    """ update city with its id"""
    if not request.get_json():
        abort(400, "Not a JSON")

    ignored_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for city in storage.all('City').values():
        if city.id == city_id:
            for k, v in request.get_json().items():
                if k not in ignored_keys:
                    setattr(city, k, v)
            city.save()
            return jsonify(city.to_dict())
    abort(404)
