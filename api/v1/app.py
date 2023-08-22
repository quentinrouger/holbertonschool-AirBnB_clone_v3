#!/usr/bin/python3
""" app of the version 1 of the API"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from flask import jsonify


app = Flask(__name__)

app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    """handler for 404 errors that returns a JSON-formatted 404 status code"""
    response = jsonify({"error": "Not found"}), 404
    return response


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', threaded=True)
