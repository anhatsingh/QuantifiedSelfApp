import email
from flask import current_app as app
from flask import jsonify, make_response, request
import flask_login
from application.models import *
from flask_restful import Resource, Api, fields, marshal_with, reqparse
from datetime import datetime
from flask_security.utils import hash_password, verify_password

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

# based on date we get from JavaScript, DO NOT CHANGE
date_format = '%m/%d/%Y, %I:%M:%S %p'

api = Api(app)
jwt = JWTManager(app)

def show_404():
    return make_response(jsonify({"msg": "The requested resource was not found on this server"}), 404)

def show_500():
    return make_response(jsonify({"msg": "Internal server error occurred"}), 500)


@app.route("/api/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(email=email).one_or_none()

    if user and verify_password(password, user.password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token)
    
    return jsonify({"msg": "Bad username or password"}), 401

    


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/api/test_login", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


class Each_Tracker_api(Resource):
    @jwt_required()
    def get(self, id):
        try:
            user_id = get_jwt_identity()
            tracker_data = Tracker.query.filter_by(user_id=user_id, id=id).one_or_none()
            if tracker_data:
                datatypes = list(set([i.datatype for i in tracker_data.ttype]))
                data = {
                    'id': tracker_data.id,
                    'name': tracker_data.name,
                    'description': tracker_data.description,
                    'type': datatypes[0] if len(datatypes) > 0 else '',
                    'settings': [i.value for i in tracker_data.settings]
                }
                if data['type'] == 'ms':
                    data['choices'] = []
                    for i in tracker_data.ttype:
                        data['choices'].append({"id": i.id, "value": i.value})
                else:
                    data['choices'] = None

                return make_response(jsonify(data), 200)
            else:
                return show_404()
        except:
            app.logger.exception("API_ETA1")
            return show_500()


tracker_input_args = reqparse.RequestParser()
tracker_input_args.add_argument('name')
tracker_input_args.add_argument('description')
tracker_input_args.add_argument('settings')
tracker_input_args.add_argument('type')
tracker_input_args.add_argument('choices')

class Trackers_api(Resource):
    @jwt_required()
    def get(self):
        try:
            user_id = get_jwt_identity()
            all_tracker_data = Tracker.query.filter_by(user_id=user_id).all()
            if all_tracker_data:
                final_data = []
                for tracker_data in all_tracker_data:
                    datatypes = list(set([i.datatype for i in tracker_data.ttype]))
                    data = {
                        'id': tracker_data.id,
                        'name': tracker_data.name,
                        'description': tracker_data.description,
                        'type': datatypes[0] if len(datatypes) > 0 else '',
                        'settings': [i.value for i in tracker_data.settings]
                    }
                    if data['type'] == 'ms':
                        data['choices'] = []
                        for i in tracker_data.ttype:
                            data['choices'].append({"id": i.id, "value": i.value})
                    else:
                        data['choices'] = None
                    
                    final_data.append(data)
                return make_response(jsonify(final_data), 200)
            else:
                return show_404()
        except:
            app.logger.exception("API_TA1")
            return show_500()
    


    def post(self):
        args = tracker_input_args.parse_args()
        name = args.get('name', None)
        description = args.get('description', None)
        settings = args.get('settings', None)
        type = args.get('type', None)
        choices = args.get('choices', None)


class Logs_api(Resource):
    @jwt_required()
    def get(self, tracker_id):
        try:
            user_id = get_jwt_identity()
            tracker_data = Tracker.query.filter_by(user_id=user_id, id=tracker_id).one_or_none()
            if tracker_data:
                datatypes = list(set([i.datatype for i in tracker_data.ttype]))
                tdata = {
                    'id': tracker_data.id,
                    'name': tracker_data.name,
                    'description': tracker_data.description,
                    'user_id': tracker_data.user_id,
                    'settings': ",".join([i.value for i in tracker_data.settings]),
                    'type': datatypes[0] if len(datatypes) > 0 else '',
                    'choices': {i.id: (i.value.strip() if i.value else '') for i in tracker_data.ttype}
                }
                
                all_log_data = Tracker_log.query.filter_by(tracker_id=tracker_data.id).all()
                if all_log_data:
                    final_data = []
                    for log_data in all_log_data:
                        ldata = {
                            'id': log_data.id,
                            'timestamp': datetime.strftime(log_data.timestamp, date_format),
                            'note': log_data.note
                        }                    
                        if tdata['type'] == 'ms':
                            ldata['value'] = []
                            for i in log_data.values:
                                choice = Tracker_type.query.filter_by(id=i.value).one_or_none()
                                ldata['value'].append({"choice_id": choice.id, "choice_name": choice.value})
                        
                        elif tdata['type'] == 'integer':
                            ldata['value'] = int(log_data.values[0].value)
                        
                        elif tdata['type'] == 'float':
                            ldata['value'] = float(log_data.values[0].value)
                        
                        final_data.append(ldata)
                    
                    return make_response(jsonify(final_data), 200)
                else:
                    return show_404()
            else:
                return show_404()
        except:
            app.logger.exception("API_LA1")
            return show_500()

api.add_resource(Each_Tracker_api, "/api/tracker/<int:id>")
api.add_resource(Trackers_api, "/api/tracker")
api.add_resource(Logs_api, "/api/tracker/<int:tracker_id>/logs")