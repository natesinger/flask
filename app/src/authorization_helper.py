# Inheretance from main
from __main__ import (
    database
)

# Python standard libraries
from functools import wraps

# Third-party libraries
import logging
from flask import (
    redirect,
    request
)


def require_role(required_role:str):
    def require_role_inner(function):
        @wraps(function)
        def authenticate(*args, **kwargs):
            # Retrieve and decode token, else error
            if not "Authorization" in request.cookies: return redirect("login")

            # Ensure the token was extracted
            authorization_token = request.cookies['Authorization'].split(' ')[1]
            if not authorization_token: return redirect("login")

            # Ensure a uid was retreived from the session
            retreived_uid = database.lookup_uid_by_session(authorization_token)
            if not retreived_uid: return redirect("login")

            # Ensure roles were retreived from the session
            retreived_roles = database.lookup_role_by_uid(retreived_uid)            
            if not retreived_roles: return redirect("login")

            # Validate that required_role in user roles
            if not required_role in retreived_roles.split(','): return redirect("login")

            return function(*args, **kwargs)
        return authenticate
    return require_role_inner