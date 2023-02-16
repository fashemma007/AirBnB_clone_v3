#!/usr/bin/python3
"""
Creating a new view for city objects that handles all default RESTFul API
actions:
"""
from models import storage
from models.city import City
from models.state import State

from flask import Flask, jsonify, abort, make_response, request
from api.v1.views import app_views


@app_views.route('/states/<string:state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_city(state_id):
    """retrieve a list of all City objects of a State"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    all_cities = []
    for city in state.cities:
        all_cities.append(city.to_dict())
    return jsonify(all_cities)


@app_views.route('/cities/<string:city_id>', strict_slashes=False)
def get_city(city_id):
    """Retrieve state object
    """
    city = storage.get(City, city_id)
    # print(city)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<string:city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """deletes city object
    """
    city = storage.get(City, city_id)
    # print(city)
    if city is None:
        abort(404)
    city.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/cities', methods=['POST'], strict_slashes=False)
def post_city():
    """creates a new city
    """
    if not request.is_json:
        abort(400, 'Not a JSON')
    else:
        request_body = request.get_json()

    if 'name' not in request_body:
        abort(400, "Missing name")
    else:
        city = City(**request_body)
        storage.new(city)
        storage.save()
        return jsonify(city.to_dict()), 201


@app_views.route('/cities/<string:city_id>',
                 methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """updates city
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, val in request.get_json().items():
        # print(city)
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, val)
    city.save()
    return jsonify(city.to_dict())
