#!/usr/bin/env python3
""" A simple flask app.
"""

from flask import Flask, jsonify, Response, request, abort
from auth import Auth
from typing import Tuple, Union
from typing_extensions import Literal

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def index() -> Response:
    """ General default
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register() -> Union[Tuple[Response, Literal[int]], Response]:
    """ Registers a user
    """
    try:
        user = AUTH.register_user(
            email=request.form.get('email'),
            password=request.form.get('password')
        )
        return jsonify({"email": user.email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login() -> Union[Tuple[Response, Literal[int]], Response, None]:
    """ User login end-point
    """
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        if AUTH.valid_login(
                email=email,
                password=password
                ):
            response = jsonify({"email": email, "message": "logged in"})
            response.set_cookie("session_id", AUTH.create_session(email=email))
            return response
    except Exception:
        pass
    else:
        return abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout() -> Union[Tuple[Response, Literal[int]], Response, None]:
    """ User logout end-point
    """
    try:
        user = AUTH.get_user_from_session_id(request.args.get('session_id'))
        if user:
            AUTH.destroy_session(user.id)
    except Exception:
        pass
    else:
        return abort(403)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
