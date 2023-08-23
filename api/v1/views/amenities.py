#!/usr/bin/python3
"""This module contains the Amenity class"""

from models.amenity import Amenity
from models import storage
from flask import jsonify, request
from api.v1.views import app_views


@app_views.route('/amenities/', methods=['GET'],
                 strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenities(amenity_id=None):
    """Retrieves get method for all amenities"""

    all_amenity = storage.all(Amenity).values()
    if amenity_id is None:
        list_amenity = []
        for amenity in all_amenity:
            list_amenity.append(amenity.to_dict())
        return jsonify(list_amenity)
    else:
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            return jsonify({'error': 'Amenity not found'}), 404
        return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify({'error': 'Amenity not found'}), 404
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def create_amenity():

    request_data = request.get_json()
    if not request_data:
        return jsonify({'error': 'Not a JSON'}), 400
    if "name" not in request_data:
        return jsonify({'error': 'Missing name'}), 400
    new_object = Amenity(**request_data)
    new_object.save()
    return jsonify(new_object.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):

    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        return jsonify({'error': 'State not Found'}), 404
    req_json = request.get_json()
    if not req_json:
        return jsonify({'error': 'Not a JSON'}), 400
    for key, value in req_json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity_obj, key, value)
    amenity_obj.save()
    return jsonify(amenity_obj.to_dict()), 200
