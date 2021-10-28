from flask import json, jsonify, abort
from werkzeug.wrappers import response
from database.operations import search_time, get_all

def __generate_json(results):
    data = []
    line = 0

    for row in results:
        r = [row.week, row.year, row.primary, row.secundary, 
            row.tertiary, row.share_count, row.share_amount, row.draw_type]
        data.insert(line, r)
        line+=1
    
    response = jsonify({'data': data})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

def get_json(all=True, week = None, year = None):
    if all==True:
        results = get()
        return __generate_json(results)
    elif (week!=None) & (year!=None):
        results = search_time(search_terms[0],search_terms[1])
        return __generate_json(results)
    else:
        abort(404)