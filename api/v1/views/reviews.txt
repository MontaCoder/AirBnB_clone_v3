#!/usr/bin/python3
""" States view """
from api.v1.views import app_views
from flask import jsonify, Blueprint, abort, request
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def all_states():
    """ Retrieves the list of all State objects """
    all_states = []
    for obj in storage.all("State").values():
        all_states.append(obj.to_dict())
    return jsonify(all_states)


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE'])
def get_state(state_id):
    """ Retrieves a State object """
    for obj in storage.all("State").values():
        if obj.id == state_id:
            if request.method == 'GET':
                return jsonify(obj.to_dict())
            if request.method == 'DELETE':
                storage.delete(obj)
                storage.save()
                return jsonify({}), 200
    abort(404)


@app_views.route('/states/', strict_slashes=False, methods=['POST'])
def create_state():
    """ Creates a State """
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    states = []
    new_state = State(name=request.json['name'])
    storage.new(new_state)
    storage.save()
    states.append(new_state.to_dict())
    return jsonify(states[0]), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def updates_state(state_id):
    """ Updates a State object """
    all_states = storage.all("State").values()
    state_obj = [obj.to_dict() for obj in all_states if obj.id == state_id]
    if state_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    state_obj[0]['name'] = request.json['name']
    for obj in all_states:
        if obj.id == state_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(state_obj[0]), 200
