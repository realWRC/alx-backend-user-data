#!/usr/bin/env python3
"""
Module for password hashing.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hasses a given password"""
    password_bytes = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed_password
