#!/usr/bin/env python3
""" This holds files for multiple functions
"""

import bcrypt
from db import DB
from typing import Union
from user import User
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ Creates a hash of input password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """ Creates a unique ID
    """
    return str(uuid4())


class Auth:
    """ Auth class to interact with the authentication database.
    """

    def __init__(self):
        """ Initialises the class
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Registers a user to a database
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            user = self._db.add_user(
                email=email,
                hashed_password=_hash_password(password),
            )
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """ Validates a user
        """
        try:
            user = self._db.find_user_by(email=email)
            if user and bcrypt.checkpw(
                    password.encode('utf-8'),
                    user.hashed_password
            ):
                return True
            else:
                return False
        except Exception:
            return False

    def create_session(self, email: str) -> Union[str, None]:
        """ Generates a session ID
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                user.session_id = _generate_uuid()
                return user.session_id
        except Exception:
            pass

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """ Retrieves user bases on session_id
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
            if user:
                return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ Destroys a user session_id
        """
        try:
            user = self._db.find_user_by(id=user_id)
            if user:
                delattr(user, 'session_id')
        except Exception:
            pass
