#!/usr/bin/python3
"""This module contains the State class"""


from models.user import User
from models import storage
from flask import jsonify, request
from api.v1.views import app_views


@app_views.route('/users/', methods=['GET'],
                 strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_users(user_id=None):
    """Retrieves get method for all state"""

    all_user = storage.all(User).values()
    if user_id is None:
        list_user = []
        for user in all_user:
            list_user.append(user.to_dict())
        return jsonify(list_user)
    else:
        user = storage.get(User, user_id)
        if user is None:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a State object"""
    user = storage.get(User, user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=['POST'], strict_slashes=False)
def create_user():

    request_data = request.get_json()
    if not request_data:
        return jsonify({'error': 'Not a JSON'}), 400
    if "email" not in request_data:
        return jsonify({'error': 'Missing email'}), 400
    if "password" not in request_data:
        return jsonify({'error': 'Missing password'}), 400
    new_object = User(**request_data)
    new_object.save()
    return jsonify(new_object.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):

    user_obj = storage.get(User, user_id)
    if user_obj is None:
        return jsonify({'error': 'User not Found'}), 404
    req_json = request.get_json()
    if not req_json:
        return jsonify({'error': 'Not a JSON'}), 400
    for key, value in req_json.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user_obj, key, value)
    user_obj.save()
    return jsonify(user_obj.to_dict()), 200
