#!/usr/bin/python3
"""API setup
"""
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
cors = CORS(app, origins='0.0.0.0', )
app.register_blueprint(app_views)


@app.teardown_appcontext
def end_session(exception):
    """Calls on storage.close method
    """
    return storage.close()


@app.errorhandler(404)
def not_found(error):
    """Page not found error handler
    """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    HOST = getenv('HBNB_API_HOST', default='0.0.0.0')
    PORT = getenv('HBNB_API_PORT', default=5002)
    app.run(host=HOST, port=PORT, threaded=True, debug=True)
