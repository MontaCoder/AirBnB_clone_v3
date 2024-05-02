#!/usr/bin/python3
""" view for user objects that handles all default RESTFul API actions """

from api.v1.views import app_views
from flask import jsonify, Blueprint, abort, request
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def get_users():
    """ Retrieves the list of all user objects """
    users = []
    for obj in storage.all('User').values():
        users.append(obj.to_dict())
    if users == []:
        abort(404)
    return users


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE'])
def get_user(user_id):
    """ Retrieves or Deletes a user object """
    for obj in storage.all('User').values():
        if obj.id == user_id:
            if request.method == 'GET':
                return jsonify(obj.to_dict())
            if request.method == 'DELETE':
                storage.delete(obj)
                storage.save()
                return jsonify({}), 200
    abort(404)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    """ Create user """
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'email' not in request.get_json():
        abort(400, 'Missing email')
    if 'password' not in request.get_json():
        abort(400, 'Missing password')
    users = []
    new_user = User()
    for k, v in request.get_json().items():
        setattr(new_user, k, v)
    storage.new(new_user)
    storage.save()
    users.append(new_user.to_dict())
    return jsonify(users[0]), 201


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def updates_user(user_id):
    """ Updates user object """
    ignored_keys = ['id', 'email', 'created_at', 'updated_at']
    if not request.get_json():
        abort(400, "Not a JSON")

    request_key = request.get_json()
    for user in storage.all('User').values():
        if user.id == user_id:
            for k, v in request_key.items():
                if k in ignored_keys:
                    continue
                setattr(user, k, v)
            user.save()
            return jsonify(user.to_dict()), 200
    abort(404)
