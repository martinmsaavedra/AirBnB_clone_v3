#!/usr/bin/python3
"""User View"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/users/<user_id>',
                 methods=['GET', 'POST', 'DELETE', 'PUT'],
                 strict_slashes=False)
def users(user_id=None):
    new_dict = storage.all(User)
    if request.method == 'GET':
        if user_id is None:
            json = []
            for key, value in new_dict.items():
                json.append(value.to_dict())
            return jsonify(json)
        else:
            user = storage.get(User, user_id)
            if user is not None:
                return jsonify(user.to_dict())
            abort(404)
    elif request.method == 'DELETE':
        if user_id is not None:
            user = storage.get(User, user_id)
            if user is not None:
                storage.delete(user)
                storage.save()
                return jsonify({}), 200
            abort(404)
    elif request.method == 'POST':
        json = request.get_json()
        if json is None:
            abort(400, 'Not a JSON')
        if 'email' not in json.keys():
            abort(400, 'Missing email')
        if 'password' not in json.keys():
            abort(400, 'Missing password')
        new_user = User(**json)
        storage.new(new_user)
        storage.save()
        return jsonify(new_user.to_dict()), 201
    elif request.method == 'PUT':
        if user_id is not None:
            json = request.get_json()
            if json is None:
                abort(400, 'Not a JSON')
            user = storage.get(User, user_id)
            if user is not None:
                for key, value in json.items():
                    if value != 'email':
                        setattr(user, key, value)
                user.save()
                return jsonify(user.to_dict()), 200
            else:
                abort(404)
