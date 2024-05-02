#!/usr/bin/python3
""" Places_reviews view """
from api.v1.views import app_views
from flask import jsonify, Blueprint, abort, request
from models import storage
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', strict_slashes=False, methods=[
    'GET'])
def all_places_reviews(place_id):
    """ Retrieves the list of reviews of a specific place"""
    all_reviews = []
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    for review in storage.all("Review").values():
        if place_id == review.place_id:
            all_reviews.append(review.to_dict())
    return jsonify(all_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE'])
def get_review(review_id):
    """ Retrieves a review object """
    for obj in storage.all("Review").values():
        if obj.id == review_id:
            if request.method == 'GET':
                return jsonify(obj.to_dict())
            if request.method == 'DELETE':
                storage.delete(obj)
                storage.save()
                return jsonify({}), 200
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def post_new_review(place_id):
    """ add new places to a specific city """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    if "user_id" not in request.get_json():
        abort(400, "Missing user_id")
    print("i am okay")
    user = storage.get('User', request.get_json()['user_id'])
    if user is None:
        abort(404)

    if "text" not in request.get_json():
        abort(400, "Missing text")
    request.get_json()['place_id'] = place_id
    review = Review(**request.get_json())
    review.save()
    return (jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review_id(review_id):
    """ update the place with its id """
    if not request.get_json():
        abort(400, "Not a JSON")

    ignored_keys = ['id', 'place_id', 'created_at', 'updated_at', 'user_id']
    for review in storage.all("Review").values():
        if review.id == review_id:
            for key, value in request.get_json().items():
                if key not in ignored_keys:
                    setattr(review, key, value)
            review.save()
            return jsonify(review.to_dict())
    abort(404)
