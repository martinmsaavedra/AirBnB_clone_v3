#!/usr/bin/python3
"""Review View"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def all_reviews(place_id):
    place = storage.get(Place, place_id)
    if place is not None:
        if request.method == 'GET':
            reviews = storage.all(Review)
            new_list = []
            for key, value in reviews.items():
                if value.place_id == place.id:
                    new_list.append(value.to_dict())
            return jsonify(new_list)
        else:
            json = request.get_json()
            if json is None:
                abort(400, 'Not a JSON')
            if 'user_id' not in json.keys():
                abort(400, 'Missing user_id')
            if 'text' not in json.keys():
                abort(400, 'Missing text')
            user = storage.get(User, json['user_id'])
            if user is None:
                abort(404)
            json['place_id'] = place_id
            new_review = Review(**json)
            storage.new(new_review)
            storage.save()
            return jsonify(new_review.to_dict()), 201
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def reviews(review_id=None):
    review = storage.get(Review, review_id)
    if review is not None:
        if request.method == 'GET':
            return jsonify(review.to_dict())
        elif request.method == 'DELETE':
            storage.delete(review)
            storage.save()
            return jsonify({}), 200
        elif request.method == 'PUT':
            json = request.get_json()
            if json is None:
                abort(400, 'Not a JSON')
            for key, value in json.items():
                setattr(review, key, value)
            review.save()
            return jsonify(review.to_dict()), 200
    else:
        abort(404)
