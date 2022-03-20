import json
from flask import current_app as app
from application.models import *
from flask_restful import Resource, Api, fields, marshal_with, reqparse

api = Api(app)


class Tracker_api(Resource):
    pass