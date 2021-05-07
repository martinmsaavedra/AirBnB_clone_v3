#!/urs/bin/python3
'''Flask module'''

from flask import jsonify, request
from models import storage
from api.v1.views import *
from models.state import State


@app_views.route('/states/', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'])
def list_states(state_id=None):
    '''list states'''
    states = storage.all(State)
    states = list(obj.to_dict() for obj in states.values())
    if not state_id:
        return jsonify(states)
    elif state_id != None:
        for state in states:
            if state['id'] == state_id:
                return jsonify(state)
    abort(404)

@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id=None):
    '''Deletes an states by ID'''
    states = storage.all(State)
    states = list(obj.to_dict() for obj in states.values())
    if state_id:
        for index, state in enumerate(states):
            if state['id'] == state_id:
                state = storage.get(State, state_id)
                storage.delete(state)
                return jsonify({}), 200
    abort(404)

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    '''Post changes in Object state'''
    state_json = request.get_json()
    if not state_json:
        abort(400, 'Not a JSON')
    elif state_json.get("name") is None:
        abort(400, 'Missing name')
    else:
        state_obj = State(**state_json)
        state_obj.save()
        state_obj = state_obj.to_dict()
        return jsonify(state_obj), 201
    abort(404)

@app_views.route('states/<state_id>', methods=['PUT'])
def put_state(state_id=None):
    '''Update object state'''
    state_json = request.get_json()
    if not state_json:
        abort(400, 'Not a JSON')
    else:
        states = storage.all(State)
        states = list(obj.to_dict() for obj in states.values())
        if state_id:
            for index, state in enumerate(states):
                if state['id'] == state_id:
                    state = storage.get(State, state_id)
                    state.save()
                    state = state.to_dict()
                    return jsonify(state), 200
    abort(404)
