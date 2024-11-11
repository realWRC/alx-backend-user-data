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
    def __init__(self) -> None:
        """
        Initialises the Authentication class
        """
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Returns some API stuff
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ Returns some API stuff
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns 
        """
        return None
