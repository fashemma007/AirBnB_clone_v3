#!/usr/bin/python3
"""view for User object that handles all default RESTFul API actions"""
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place


@app_views.route("users", strict_slashes=False)
@app_views.route("users/<user_id>", methods=['GET'], strict_slashes=False)
def get_users(user_id=None):
    """retrieves users"""
    user_list = []
    if user_id is None:
        users = storage.all(User)
        values = [val for val in users.values()]
        user_list = [user.to_dict() for user in values]
        return jsonify(user_list), 200
    else:
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
    # print(user)
    return jsonify(user.to_dict()), 200


@app_views.route("users/<user_id>", methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """deletes a user whose id is given"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    # print(type(user))
    storage.delete(user)
    storage.save()
    return jsonify({})


@app_views.route("users/", methods=['POST'], strict_slashes=False)
@app_views.route("users/<user_id>", methods=['PUT'], strict_slashes=False)
def post_put(user_id=None):
    """Handles creation and updates of users in storage"""
    print("I'm here")
    if not request.is_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    else:
        user_info = request.get_json()
    if request.method == "POST":
        if 'email' not in user_info:
            return make_response(jsonify({'error': "Missing email"}), 400)
        elif 'password' not in user_info:
            return make_response(jsonify({'error': "Missing password"}), 400)
        new_user = User(**user_info)
        storage.new(new_user)
        storage.save()
        return jsonify(new_user.to_dict()), 201
    else:
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        user_info = request.get_json()
        for key, val in user_info.items():
            # print(city)
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(user, key, val)
        user.save()
    return jsonify(user.to_dict())
