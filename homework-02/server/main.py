#!/usr/bin/env python3

from bottle import route, run
from bottle import request, response
from bottle import Bottle
import json
import psycopg2

dbname = 'simple'
user = 'Qwerty'
dbhost = 'database'
password = 'Qwerty5432'

app = Bottle()


@app.route('/', method='GET')
def get_data():
    global dbname, user, dbhost, password
    res = None
    with psycopg2.connect(dbname=dbname, user=user, host=dbhost, password=password) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tbl;")
            res = cur.fetchall()

    if res is not None:
        res = [(key, value) for _, key, value in res]
        res = json.dumps(dict(res))
        response.status = 200
    else:
        res = "\n"
        response.status = 500
    
    return res


@app.route('/health', method='GET')
def check_health():    
    response.status = 200
    return "Server alive"


@app.error(404)
def not_found(error):
    response.status = 404
    return "Page not found"


app.run(host='0.0.0.0', port=5001)