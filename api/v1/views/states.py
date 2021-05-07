#!/urs/bin/python3
'''Flask module'''


from flask import jsonify
from models import storage
from api.v1.views import app_views
from models.state import State

@app_views.route('/states', methods=['GET'])
def list_states():
    '''list states'''
    states = storage.all(State)
    states = list(obj.to_json() for obj in states.values())
    return jsonify(states)



    
