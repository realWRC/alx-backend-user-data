#!/usr/bin/env python3
"""
Authentication handling for the testing API
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """
    Defines the Authentication for the API
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Returns some API stuff
        """
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        if path in excluded_paths:
            return False

        for excluded_path in excluded_paths:
            if excluded_path.startswith(path):
                return False
            elif path.startswith(excluded_path):
                return False
            elif excluded_path[-1] == "*":
                if path.startswith(excluded_path[:-1]):
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Returns some API stuff
        """
        if request is None:
            return None

        return request.headers.get('Authorization')


    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns
        """
        return None
