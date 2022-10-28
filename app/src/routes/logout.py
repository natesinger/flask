# Inheretance from main
from __main__ import app

# Third-party libraries
import logging
from flask import (
    redirect,
    request
)

# Internal imports
from src.session_helper import purge_session
from src.authorization_helper import require_role


@app.route("/logout")
@require_role("guest")
def logout():
    authorization_header = request.cookies['Authorization']
    session_token = authorization_header.split(' ')[1]
    
    purge_session(session_token)
    return redirect('/')
