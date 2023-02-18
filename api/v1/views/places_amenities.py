#!/usr/bin/python3
"""view for the link between Place objects and Amenity objects"""
from flask import make_response, abort, jsonify
from api.v1.views import app_views
from models.amenity import Amenity
from models.place import Place
from models import storage, storage_t


@app_views.route(
    'places/<place_id>/amenities', methods=["GET"], strict_slashes=False
)
def all_amenities(place_id):
    """Retrieves a list of all amenities available in a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if storage_t == 'db':
        return jsonify([amenity.to_dict() for amenity in place.amenities])
    else:
        return jsonify([
            storage.get(Amenity, a_id).to_dict() for a_id in place.amenity_ids
        ])


@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>",
    methods=["DELETE"], strict_slashes=False
)
def delete_place_amenity(place_id, amenity_id):
    """Delete a Amenity object by its id from a Place object"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if storage_t == "db":
        if amenity not in place.amenities:
            abort(404)
    else:
        if amenity.id not in place.amenity_id:
            abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route(
    "places/<place_id>/amenities/<amenity_id>",
    methods=["POST"],
    strict_slashes=False
)
def add_amenity_for_place(place_id, amenity_id):
    """Insert new amenity object into Place object"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if storage_t == "db":
        if amenity in place.amenities:
            return jsonify(amenity.to_dict())
        else:
            place.amenities.append(amenity)
    else:
        if amenity.id in place.amenity_id:
            return jsonify(amenity.to_dict())
        else:
            place.amenity_id.append(amenity.id)
    storage.save()
    return jsonify(amenity.to_dict()), 201
