import json
from flask import Flask
from flask import Response
from flask import Blueprint
from swagger_ui import flask_api_doc

__author__ = "Mirco Manzoni"
__credits__ = ["Mirco Manzoni"]
__status__ = "Development"

DEBUG_PREFIX = 'debug'
API_PREFIX = ''

debug_page = Blueprint(DEBUG_PREFIX, __name__)


@debug_page.route('/')
def hello():
    resp = {'msg': 'This is the REST API for debugging of DUE-VDM'}
    return Response(json.dumps(resp), status=200, mimetype='application/json')


@debug_page.route('/vdcs')
def get_vdcs():
    resp = ['a', 'b', 'c']
    return Response(json.dumps(resp), status=200, mimetype='application/json')


@debug_page.route('<string:vdc>/methods')
def get_methods(vdc):
    resp = ['a', 'b', 'c']
    return Response(json.dumps(resp), status=200, mimetype='application/json')


app = Flask(__name__)
app.debug = True

# API v1
app.register_blueprint(debug_page, url_prefix=API_PREFIX + '/' + DEBUG_PREFIX)


@app.route('/')
def index():
    resp = {'msg': 'This is the REST API of DUE-VDM'}
    return Response(json.dumps(resp), status=200, mimetype='application/json')


# Generating the docs
flask_api_doc(app, config_path='./specs.yaml', url_prefix='/api/doc', title='API doc')