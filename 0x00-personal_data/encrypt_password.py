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


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if a password is valid"""
    password_bytes = password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password)
