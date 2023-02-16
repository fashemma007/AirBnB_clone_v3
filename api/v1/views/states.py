#!/usr/bin/python3
"""
Creating a new view for State objects that handles all default RESTFul API actions:
"""
from models import storage
from models.state import State

from flask import Flask, jsonify, abort, make_response, request
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects
    """
    all_states = []
    states = storage.all(State).values()
    for state in states:
        all_states.append(state.to_dict())
    return jsonify(all_states)


@app_views.route('/states/<string:state_id>', strict_slashes=False)
def get_state(state_id):
    """Retrieve state object
    """
    state = storage.get(State, state_id)
    # print(state)
    if state:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<string:state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """deletes state object
    """
    state = storage.get(State, state_id)
    # print(state)
    if state is None:
        abort(404)
    state.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """creates a new state
    """
    if not request.is_json:
        abort(400, 'Not a JSON')
    else:
        request_body = request.get_json()

    if 'name' not in request_body:
        abort(400, "Missing name")
    else:
        state = State(**request_body)
        storage.new(state)
        storage.save()
        return jsonify(state.to_dict()), 201


@app_views.route('/states/<string:state_id>',
                 methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """updates state
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, val in request.get_json().items():
        # print(val)
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, val)
    state.save()
    return jsonify(state.to_dict())
