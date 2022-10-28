# Python standard libraries
import json
import os
import sqlite3

# Third-party libraries
from flask import (
    Flask, 
    render_template,
    redirect,
    request,
    url_for
)
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from urllib import parse
from oauthlib.oauth2 import WebApplicationClient
import requests
import logging

# Internal imports
from src.sso_helper import retrieve_jwks, decode_retreived_jwt

# Environment
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
HOST_AND_PORT = os.environ.get("HOST_AND_PORT", None)
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"


app = Flask(__name__, template_folder="pages", static_folder="public", static_url_path="/public")
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)


@app.route("/")
def index(): return redirect("/login")


@app.route("/login", methods=['GET', 'POST'])
def login():
    # provide authentication page
    if request.method == 'GET': 
        return render_template("login.html",
                               host_port=HOST_AND_PORT,
                               google_client_id=GOOGLE_CLIENT_ID
                            )

    # attempt authentication via provided data
    if request.method == 'POST':

        # if we got plaintext user and password attempt
        if "username" in request.get_data().decode('ascii'):
            attempted_username = request.form['username']
            attempted_password = request.form['password']

            logging.info(f"Credential login attempted with '{attempted_username}:{attempted_password}'")
            return render_template("login.html",
                                   host_port=HOST_AND_PORT,
                                   google_client_id=GOOGLE_CLIENT_ID,
                                   bad_login="credentials"
                                )
        
        # assume the user is attempting SSO
        else:
            query_string = request.get_data().decode('ascii')

            unverified_jwt = parse.parse_qs(query_string)['credential'][0]

            logging.info(f"SSO login attempted with '{unverified_jwt}'")
            
            return decode_retreived_jwt(unverified_jwt, retrieve_jwks(), GOOGLE_CLIENT_ID)

            return render_template("login.html",
                                   host_port=HOST_AND_PORT,
                                   google_client_id=GOOGLE_CLIENT_ID,
                                   bad_login="credentials"
                                )



"""
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
"""

@app.route("/about")
def about(): 
    return render_template("about.html")


# start application
if __name__ == "__main__": app.run(ssl_context="adhoc", debug=True)