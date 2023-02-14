#!/usr/bin/python3
"""Index Package"""
from flask import jsonify
from models import storage
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """JSON response giving the api status
    """
    return jsonify({"status": "OK"})

amenities_ = storage.count(Amenity)
cities_ = storage.count(City)
places_ = storage.count(Place)
reviews_ = storage.count(Review)
states_ = storage.count(State)
users_ = storage.count(User)

info = {"amenities": amenities_,
        "cities": cities_,
        "places": places_,
        "reviews": reviews_,
        "states": states_,
        "users": users_}

@app_views.route('/stats', strict_slashes=False)
def object_numb():
    """an endpoint that retrieves the number of each objects by type"""
    return jsonify(info)