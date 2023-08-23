#!/usr/bin/python3
"""This module contains the City class"""

from models.review import Review
from models.user import User
from models.place import Place
from models.city import City
from models import storage
from flask import jsonify, request
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_places_review(place_id):
    """Retrieves get method for all place_review"""

    place_id = storage.get(Place, place_id)
    if place_id is None:
        return jsonify({'error': 'Review not found'}), 404
    return jsonify([review.to_dict() for review in place_id.reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_place_review(review_id):
    """Retrieves place_review by a place_review_id"""
    review = storage.get(Review, review_id)
    if review is None:
        return jsonify({"error": "Review not found"}), 404
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place_review(review_id):
    """Delete a place_review object"""
    review = storage.get(Review, review_id)
    if review is None:
        return jsonify({'error': 'Review not found'}), 404
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def create_place_review(place_id):
    """Create a new place_review"""
    request_data = request.get_json()
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({'error': 'Place not found'}), 404
    if not request_data:
        return jsonify({'error': 'Not a JSON'}), 400
    if "user_id" not in request_data:
        return jsonify({'error': 'Missing user_id'}), 400
    user_id = request_data.get("user_id")
    user = storage.get(User, user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    if "text" not in request_data:
        return jsonify({'error': 'Missing text'}), 400

    new_object = Review(**request_data)
    new_object.place_id = place.id
    new_object.user_id = user.id
    new_object.save()
    return jsonify(new_object.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_place_review(review_id):
    """Update a place_review based on its id"""
    review_obj = storage.get(Review, review_id)
    if review_obj is None:
        return jsonify({'error': 'Review not Found'}), 404
    req_json = request.get_json()
    if not req_json:
        return jsonify({'error': 'Not a JSON'}), 400
    for key, value in req_json.items():
        if key not in ['id', 'user_id',
                       'place_id',
                       'created_at',
                       'updated_at']:
            setattr(review_obj, key, value)
    review_obj.save()
    return jsonify(review_obj.to_dict()), 200
