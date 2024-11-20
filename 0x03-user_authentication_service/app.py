#!/usr/bin/env python3
""" A simple flask app.
"""

from flask import Flask, jsonify, Response
from auth import Auth

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index() -> Response:
    """ General default
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
