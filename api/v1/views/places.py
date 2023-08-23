#!/usr/bin/python3
"""This module contains the City class"""

from models.user import User
from models.place import Place
from models.city import City
from models import storage
from flask import jsonify, request
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves get method for all place"""

    city_id = storage.get(City, city_id)
    if city_id is None:
        return jsonify({'error': 'Place not found'}), 404
    return jsonify([place.to_dict() for place in city_id.places])


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieves place by a place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Place not found"}), 404
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Delete a place object"""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({'error': 'Place not found'}), 404
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Create a new place"""
    request_data = request.get_json()
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({'error': 'Place not found'}), 404
    if not request_data:
        return jsonify({'error': 'Not a JSON'}), 400
    if "user_id" not in request_data:
        return jsonify({'error': 'Missing user_id'}), 400
    user_id = request_data.get("user_id")
    user = storage.get(User, user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    if "name" not in request_data:
        return jsonify({'error': 'Missing name'}), 400

    new_object = Place(**request_data)
    new_object.city_id = city.id
    new_object.user_id = user.id
    new_object.save()
    return jsonify(new_object.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """Update a place based on its id"""
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        return jsonify({'error': 'Place not Found'}), 404
    req_json = request.get_json()
    if not req_json:
        return jsonify({'error': 'Not a JSON'}), 400
    for key, value in req_json.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place_obj, key, value)
    place_obj.save()
    return jsonify(place_obj.to_dict()), 200
