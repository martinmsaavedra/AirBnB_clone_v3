#!/usr/bin/python3
"""Amenity View"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>',
                 methods=['GET', 'POST', 'DELETE', 'PUT'],
                 strict_slashes=False)
def amenities(amenity_id=None):
    new_dict = storage.all(Amenity)
    if request.method == 'GET':
        if amenity_id is None:
            json = []
            for key, value in new_dict.items():
                json.append(value.to_dict())
            return jsonify(json)
        else:
            amenity = storage.get(Amenity, amenity_id)
            if amenity is not None:
                return jsonify(amenity.to_dict())
            abort(404)
    elif request.method == 'DELETE':
        if amenity_id is not None:
            amenity = storage.get(Amenity, amenity_id)
            if amenity is not None:
                storage.delete(amenity)
                storage.save()
                return jsonify({}), 200
            abort(404)
    elif request.method == 'POST':
        json = request.get_json()
        if json is None:
            abort(400, 'Not a JSON')
        if 'name' not in json.keys():
            abort(400, 'Missing name')
        else:
            new_amenity = Amenity(**json)
            storage.new(new_amenity)
            storage.save()
            return jsonify(new_amenity.to_dict()), 201
    elif request.method == 'PUT':
        if amenity_id is not None:
            json = request.get_json()
            if json is None:
                abort(400, 'Not a JSON')
            amenity = storage.get(Amenity, amenity_id)
            if amenity is not None:
                for key, value in json.items():
                    setattr(amenity, key, value)
                amenity.save()
                return jsonify(amenity.to_dict()), 200
            else:
                abort(404)
