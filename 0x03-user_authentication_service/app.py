#!/usr/bin/env python3
""" A simple flask app.
"""

from flask import Flask, jsonify, Response, request
from sqlalchemy import Integer
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


# def register() -> Union[Tuple[Response, Literal[int]], Response]:
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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
