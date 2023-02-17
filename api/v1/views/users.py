#!/usr/bin/python3
"""view for User object that handles all default RESTFul API actions"""
from flask import abort, jsonify, make_response
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("users", strict_slashes=False)
@app_views.route("users/<user_id>", methods=['GET'], strict_slashes=False)
def get_users(user_id=None):
    """retrieves users"""
    user_list = []
    if user_id is None:
        users = storage.all(User)
        values = [val for val in users.values()]
        user_list = [user.to_dict() for user in values]
        if len(user_list) == 0:
            abort(404)
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
# "Not a JSON"


# "Missing email"
