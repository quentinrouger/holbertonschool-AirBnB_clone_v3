#!/usr/bin/python3
""" index """

from flask import Response
import json
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def return_status():
    response_data = {"status": "OK"}
    response = Response(json.dumps(response_data),
                        content_type='application/json')
    return response
