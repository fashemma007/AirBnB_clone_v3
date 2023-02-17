#!/usr/bin/python3
"""Views for place objects"""

from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models.city import City
from models import storage
from models.place import Place
from models.user import User


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


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a place object from storage
    ::param place_id -> id of the place to return
    Returns: empty json response `200`
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a place object
    ::param city_id -> id of the city to create new place in
    Returns: json response of new object `201`
    """
    if storage.get(City, city_id) is None:
        abort(404)
    if not request.is_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    place = request.get_json()
    if 'user_id' not in place:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    elif 'name' not in place:
        return make_response(jsonify({"error": "Missing name"}), 400)
    user_id = place.get('user_id')
    if storage.get(User, user_id) is None:
        abort(404)
    place.update(city_id=city_id)
    new_place = Place(**place)
    new_place.save()
    return make_response(jsonify(new_place.to_dict())), 201


@app_views.route('places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """updates the info of a place object
    ::param place_id -> id of the place object to update
    Returns: json response of new object `200`
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    try:
        info = request.get_json()
    except Exception:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in info.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return make_response(jsonify(place.to_dict())), 200
