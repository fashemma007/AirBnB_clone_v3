#!/usr/bin/python3
"""handles all default RESTFul API actions for City objects"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route("amenities", methods=["GET"], strict_slashes=False)
@app_views.route("amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenities(amenity_id=None):
    """retrieves list of all amenities
    """
    if amenity_id is None:
        amenity = []
        amenities = storage.all(Amenity).values()
        [amenity.append(amens.to_dict()) for amens in amenities]
        return jsonify(amenity)
    else:
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("amenities", methods=["POST"], strict_slashes=False)
@app_views.route("amenities/<amenity_id>", methods=["PUT"], strict_slashes=False)
def create_amenities(amenity_id=None):
    """creates and updates amenities
    """
    if request.get_json():
        if request.method == "POST":
            req = request.get_json()
            amenity = Amenity(**req)
            storage.new(amenity)
            storage.save()
        else:
            amenity = storage.get(Amenity, amenity_id)
            for key, val in request.get_json().items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(amenity, key, val)
    amenity.save()
    return jsonify(amenity.to_dict())
