#!/usr/bin/env python3
""" This holds files for multiple functions
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """ Creates a hash of input password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
