from flask import Flask, render_template, request, redirect, session, url_for
from functools import wraps
from hashlib import sha256
import requests
import json

## Flask_MongoDB imports
from mongo import mongo

## Flask_REST API imports
from flask_restful import Api
from api.resources.data import Data
from api.resources.pubg import PUBG


'''
Init
'''
app = Flask(__name__)

# set the secret key. keep this really secret:
app.secret_key = 'V\xd7Hv\x95\x84\x06\xa2&\xc9T\x96\n\xb0I\x88\xa6\x1694\x03&\x17\xdb'

# Load app configs from config.py
app.config.from_object('config')

# Init the mongo flask instance
mongo.init_app(app)


'''
Utilities
'''
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            session['username']
        except KeyError:
            return redirect(url_for('landing'))
        return f(*args, **kwargs)

    return decorated_function


'''
Web Page Routes
'''
@app.route("/", methods=['GET'])
def landing():
    return render_template("landing/index.html")


@app.route("/admin/login", methods=['POST'])
def login():
    if request.form['username'] and request.form['password']:
        form_username = request.form['username']
        form_password = request.form['password']
        form_hash = sha256(form_password).hexdigest()
        # check with db
        mcol = mongo.db['dashy-users']
        mdata = mcol.find_one({"username": form_username})
        if mdata:
            if form_hash == mdata['password']:
                session['username'] = request.form['username']
                return redirect(url_for('dashboard'))
    return redirect(url_for('landing'))


@app.route("/admin/logout", methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('landing'))


@app.route("/admin/dashboard", methods=['GET'])
@login_required
def dashboard():
    return render_template("admin/dashboard.html")


@app.route("/admin/databases", methods=['GET'])
@login_required
def databases():
    return render_template("admin/databases.html")


@app.route("/admin/servers", methods=['GET'])
@login_required
def servers():
    return render_template("admin/servers.html")


@app.route("/ajax/nagios", methods=['GET'])
@login_required
def nagios():
    url = "http://nagios.nathanglover.com:8084/state"
    headers = {
        'content-type': "application/json"
    }
    response = requests.request("GET", url, headers=headers)
    return response.text


'''
API Definitions
'''
api = Api(app)

api.add_resource(Data, "/api/v1/data", "/api/v1/data/")
api.add_resource(PUBG, "/api/v1/pubg", "/api/v1/pubg/")


if __name__ == '__main__':
    app.run(host='0.0.0.0')
