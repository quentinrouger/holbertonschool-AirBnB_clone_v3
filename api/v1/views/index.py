#!/usr/bin/python3
""" index """

from flask import Response, jsonify
import json
from api.v1.views import app_views
from models import storage


@app_views.route('/status', strict_slashes=False)
def return_status():
    response_data = {"status": "OK"}
    response = Response(json.dumps(response_data),
                        content_type='application/json')
    return response

@app_views.route('/stats', strict_slashes=False)
def get_stats():
    """
    Retrieves the number of each type of object
    """
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    }
    return jsonify(stats)
