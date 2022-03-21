from flask import current_app as app
from flask import jsonify, request
from application.models import *
from flask_security.utils import verify_password
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

from .response_codes import *

# ============================================================================AUTHORIZATION======================================================================
@app.route("/api/login", methods=["POST"])
def login():
    try:
        email = request.json.get("email", None)
        password = request.json.get("password", None)
        user = User.query.filter_by(email=email).one_or_none()

        if user and verify_password(password, user.password):
            access_token = create_access_token(identity=user.id)
            return jsonify(token=access_token), 200
        
        return jsonify({"msg": "Bad username or password"}), 401
    except:
        app.logger.exception("API_LOGIN: Error occurred")
        return show_500()

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/api/test", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# ==============================================================================================================================================================