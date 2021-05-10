#!/usr/bin/python3
'''Flask module'''

from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def list_cities(state_id=None):
    '''list states'''
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities_list = []
    for city in state.cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def retrieve_city(city_id=None):
    '''Retrieves a City'''
    city = storage.get(City, city_id)
    if city is not None:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id=None):
    '''Deletes a City Object'''
    if city_id is None:
        abort(404)
    city = storage.get(City, city_id)
    if city is not None:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id=None):
    '''Creates a City'''
    city_json = request.get_json()
    if not city_json:
        abort(400, 'Not a JSON')
    elif city_json.get("name") is None:
        abort(400, 'Missing name')
    else:
        city_json['state_id'] = state_id
        city_obj = City(**city_json)
        storage.new(city_obj)
        storage.save()
        city_obj = city_obj.to_dict()
        return jsonify(city_obj), 201
    abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id=None):
    '''Update object state'''
    city_json = request.get_json()
    if not city_json:
        abort(400, 'Not a JSON')
    elif city_id:
        city = storage.get(City, city_id)
        if city:
            for key, value in city_json.items():
                setattr(city, key, value)
            city.save()
            city = city.to_dict()
            return jsonify(city), 200
        else:
            abort(404)
