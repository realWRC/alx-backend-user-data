#!/usr/bin/env python3
""" Session authentication stuff for the views
"""

from flask import jsonify, request
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route(
    '/auth_session/login', methods=['POST'], strict_slashes=False
)
def login():
    """ Handles login stuff for security
    """
    from api.v1.app import auth

    email = request.form.get('email')
    password = request.form.get('password')

    if not email or email == '':
        return jsonify({"error": "email missing"}), 400
    if not password or password == '':
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': email})
    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user.id)
    user_json = user.to_json()
    response = jsonify(user_json)
    session_name = getenv('SESSION_NAME')

    response.set_cookie(session_name, session_id)
    return response
