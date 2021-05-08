#!/usr/bin/python3
"""Flask Model"""
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

my_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
my_port = os.getenv('HBNB_API_PORT', 5000)


@app.teardown_appcontext
def close_session(self):
    '''Close session'''
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    '''Flask App'''
    app.run(host=my_host, port=my_port, threaded=True)
