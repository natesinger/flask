# Inheretance from main
from __main__ import (
    app,
    database, 
    HOST_AND_PORT,
    GOOGLE_CLIENT_ID
)

# Python standard libraries
import os

# Third-party libraries
import logging
from urllib import parse
from flask import (
    render_template,
    redirect,
    request
)

# Internal imports
from src.sso_helper import retrieve_jwks, decode_retreived_jwt
from src.user_helper import validate_password_bcrypt
from src.session_helper import create_session

@app.route("/login", methods=['GET', 'POST'])
def login():
    # provide authentication page
    if request.method == 'GET':
        return render_template("login.html",
                               host_port=HOST_AND_PORT,
                               google_client_id=GOOGLE_CLIENT_ID)

    # attempt authentication via provided data
    if request.method == 'POST':

        # if we got plaintext user and password attempt
        if "username" in request.get_data().decode('ascii'):
            attempted_username = request.form['username']
            attempted_password = request.form['password']

            logging.info(f"Credential login attempted with '{attempted_username}:{attempted_password}'")

            retreived_account = database.lookup_by_username(attempted_username)

            # if username not in database, failure
            if not retreived_account:
                return render_template("login.html",
                                    host_port=HOST_AND_PORT,
                                    google_client_id=GOOGLE_CLIENT_ID,
                                    bad_login="credentials")

            # if password is incorrect, failure
            valid_password = retreived_account[2]
            if not validate_password_bcrypt(attempted_password, valid_password):
                return render_template("login.html",
                                    host_port=HOST_AND_PORT,
                                    google_client_id=GOOGLE_CLIENT_ID,
                                    bad_login="credentials")  

            user_id = retreived_account[0]
            session_token = create_session(user_id)

            response = redirect("/")
            response.set_cookie('Authorization', f"Bearer {session_token}")
            return response

        
        # assume the user is attempting SSO
        else:
            #retreive data and parse out the token
            query_string = request.get_data().decode('ascii')
            unverified_jwt = parse.parse_qs(query_string)['credential'][0]

            logging.info(f"SSO login attempted with '{unverified_jwt}'")

            valid_jwt = decode_retreived_jwt(unverified_jwt, retrieve_jwks(), GOOGLE_CLIENT_ID)

            # check if user exists, if not send them to registration
            if not database.lookup_by_email(valid_jwt['email']):
                # code 307 tells the browser to retain the method/content
                return redirect('/register',code=307)


            retreived_account = database.lookup_by_email(valid_jwt['email'])

            # this case should theoretically be impossible as it would be caught above
            if not retreived_account:
                return render_template("login.html",
                                   host_port=HOST_AND_PORT,
                                   google_client_id=GOOGLE_CLIENT_ID,
                                   bad_login="generic")

            user_id = retreived_account[0]
            session_token = create_session(user_id)

            response = redirect("/")
            response.set_cookie('Authorization', f"Bearer {session_token}")
            return response



            
