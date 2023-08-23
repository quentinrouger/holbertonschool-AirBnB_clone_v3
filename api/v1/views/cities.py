#!/usr/bin/python3
"""This module contains the City class"""

from models.state import State
from models.city import City
from models import storage
from flask import jsonify, request
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """Retrieves get method for all state"""

    state_id = storage.get(State, state_id)
    if state_id is None:
        return jsonify({'error': 'State not found'}), 404
    return jsonify([city.to_dict() for city in state_id.cities])


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """Retrieves city by a city_id"""
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({"error": "City not found"}), 404
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Delete a city object"""
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({'error': 'City not found'}), 404
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Create a new city"""
    request_data = request.get_json()
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({'error': 'State not found'}), 404
    if not request_data:
        return jsonify({'error': 'Not a JSON'}), 400
    if "name" not in request_data:
        return jsonify({'error': 'Missing name'}), 400

    new_object = City(**request_data)
    new_object.state_id = state.id
    new_object.save()
    return jsonify(new_object.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """Update a city based on its id"""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        return jsonify({'error': 'State not Found'}), 404
    req_json = request.get_json()
    if not req_json:
        return jsonify({'error': 'Not a JSON'}), 400
    for key, value in req_json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city_obj, key, value)
    city_obj.save()
    return jsonify(city_obj.to_dict()), 200
