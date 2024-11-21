#!/usr/bin/env python3
""" A module to test the Flask app.
"""

import requests

BASE_URL = 'http://localhost:5000'
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """ Tests registering a user.
    """
    data = {
        'email': email,
        'password': password
    }
    response = requests.post(f'{BASE_URL}/users', data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """ Tests logging in with the wrong password.
    """
    data = {
        'email': email,
        'password': password
    }
    response = requests.post(f'{BASE_URL}/sessions', data=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """ Tests logging in.
    """
    data = {
        'email': email,
        'password': password
    }
    response = requests.post(f'{BASE_URL}/sessions', data=data)
    assert response.json() == {"email": email, "message": "logged in"}
    session_id = response.cookies.get('session_id')
    assert session_id is not None
    return session_id


def profile_unlogged() -> None:
    """ Tests accessing profile when not logged in.
    """
    response = requests.get(f'{BASE_URL}/profile')
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """ Tests accessing profile when logged in.
    """
    cookies = {'session_id': session_id}
    response = requests.get(f'{BASE_URL}/profile', cookies=cookies)
    assert 'email' in response.json()
    EMAIL = "guillaume@holberton.io"
    assert response.json() == {"email": EMAIL}


def log_out(session_id: str) -> None:
    """ Tests logging out.
    """
    cookies = {'session_id': session_id}
    response = requests.delete(
        f'{BASE_URL}/sessions', cookies=cookies, allow_redirects=False
    )
    assert response.status_code == 302
    assert response.headers['Location'] == '/'


def reset_password_token(email: str) -> str:
    """Test requesting a password reset token."""
    data = {'email': email}
    response = requests.post(f'{BASE_URL}/reset_password', data=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    assert response.status_code == 200
    print(response)
    json_response = response.json()
    assert 'reset_token' in json_response
    assert json_response['email'] == email
    reset_token = json_response['reset_token']
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Tests updating the password.
    """
    data = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    }
    response = requests.put(f'{BASE_URL}/reset_password', data=data)
    assert response.json() == {"email": email, "message": "Password updated"}


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
