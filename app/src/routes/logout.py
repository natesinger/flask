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


###### TODO MUST REQUIRE AUTHENTICATION ########
@app.route("/logout")
def logout():
    authorization_header = request.cookies['Authorization']
    session_token = authorization_header.split(' ')[1]
    
    purge_session(session_token)
    return redirect('/')
