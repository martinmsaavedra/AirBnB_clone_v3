#!/usr/bin/python3
"""Index Module"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage

# Habra que importar los objetos????


status = {'status': 'OK'}


@app_views.route('/status')
def get_status():
    '''Print status'''
    return jsonify(status)


@app_views.route('/stats')
def get_stats():
    '''Retrieves the number of each objects by type'''
    json_dic = {
        "amenities": 'Amenity',
        "cities": 'City',
        'places': 'Place',
        'state': 'State',
        'reviews': 'Review',
        'users': "User"
    }
    for key, value in json_dic.items():
        count = storage.count(value)
        json_dic[key] = count
    return jsonify(json_dic)
