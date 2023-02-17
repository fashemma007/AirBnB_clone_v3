#!/usr/bin/python3
"""Views for place objects"""

from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('places/<place_id>/reviews', strict_slashes=False)
def place_reviews(place_id):
    """Retrieves all reviews available for a given place
    ::param place_id(str) : the id of the place
    Returns: json response `200`
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = storage.all(Review)
    reviews = [review.to_dict() for review in reviews.values()]
    place_reviews = [plc
                   for plc in reviews
                   if plc.get('place_id') == place_id
                   ]
    return jsonify(place_reviews), 200


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def get_review(review_id):
    """retrieves a review object
    ::param review_id -> id of the review to return
    Returns: json response `200`
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Deletes a review object from storage
    ::param review_id -> id of the review to return
    Returns: empty json response `200`
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Creates a review object
    ::param place_id -> id of the place to create new review in
    Returns: json response of new object `201`
    """
    if storage.get(Place, place_id) is None:
        abort(404)
    if not request.is_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    review = request.get_json()
    if 'user_id' not in review:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    elif 'name' not in review:
        return make_response(jsonify({"error": "Missing name"}), 400)
    user_id = review.get('user_id')
    if storage.get(User, user_id) is None:
        abort(404)
    review.update(plce_id=place_id)
    new_review = Review(**review)
    new_review.save()
    return make_response(jsonify(new_review.to_dict())), 201


@app_views.route('reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """updates the info of a review object
    ::param review_id -> id of the review object to update
    Returns: json response of new object `200`
    """
    review = storage.get(Place, review_id)
    if review is None:
        abort(404)
    if request.is_json:
        try:
            info = request.get_json()
        except Exception as e:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
    else:
        abort(400, "Not a JSON")
    for key, value in info.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    return make_response(jsonify(review.to_dict())), 200