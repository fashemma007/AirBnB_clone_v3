#!/usr/bin/python3
"""view for User object that handles all default RESTFul API actions"""
from flask import abort, jsonify
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("users", strict_slashes=False)
def get_users(user_id=None):
    user_list = []
    if user_id is None:
        users = storage.all(User)
    else:
        users = storage.get(User, user_id)
    if not users:
        abort(404)
    values = [val for val in users.values()]
    user_list = [user.to_dict() for user in values]
    # print(user_list)
    return jsonify(user_list), 200
