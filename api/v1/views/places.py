#!/usr/bin/python3
"""Views for place objects"""

from flask import abort, jsonify
from api.v1.views import app_views
from models.city import City
from models import storage
from models.place import Place


@app_views.route('cities/<city_id>/places', strict_slashes=False)
def city_places(city_id):
    """Retrieves all places available for a given city
    ::param city_id(str) : the id of the city
    Returns: json response `200`
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = storage.all(Place)
    places = [place.to_dict() for place in places.values()]
    city_places = [plc
                   for plc in places
                   if plc.get('city_id') == city_id
                   ]
    return jsonify(city_places), 200


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place(place_id):
    """retrieves a place object
    ::param place_id -> id of the place to return
    Returns: json response `200`
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())
