#!/usr/bin/env python3
""" A session authentication implimentation
"""

from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """ A class for session authentication
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates a session ID for a user
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id
