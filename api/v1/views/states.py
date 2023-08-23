#!/usr/bin/python3
"""This module contains the State class"""


from models.state import State
from models import storage
from flask import jsonify, request
from api.v1.views import app_views


@app_views.route('/states/', methods=['GET'],
                 strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def get_states(state_id=None):
    """Retrieves get method for all state"""

    all_state = storage.all(State).values()
    if state_id is None:
        list_state = []
        for state in all_state:
            list_state.append(state.to_dict())
        return jsonify(list_state)
    else:
        state = storage.get(State, state_id)
        if state is None:
            return jsonify({'error': 'State not found'}), 404
        return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({'error': 'State not found'}), 404
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def create_state():

        request_data = request.get_json()
        if not request_data:
            return jsonify({'error': 'Not a JSON'}), 400
        if "name" not in request_data:
            return jsonify({'error': 'Missing name'}), 400
        new_object = State(**request_data)
        new_object.save()
        return jsonify(new_object.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):

    state_obj = storage.get(State, state_id)
    if state_obj is None:
        return jsonify({'error': 'State not Found'}), 404
    req_json = request.get_json()
    if not req_json:
        return jsonify({'error': 'Not a JSON'}), 400
    for key, value in req_json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state_obj, key, value)
    state_obj.save()
    return jsonify(state_obj.to_dict()), 200
