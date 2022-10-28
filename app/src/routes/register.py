# Inheretance from main
from __main__ import (
    app,
    database,
    HOST_AND_PORT,
    GOOGLE_CLIENT_ID
)

# Third-party libraries
from flask import (
    render_template,
    redirect,
    request
)
from urllib import parse
import logging

# Internal imports
from src.sso_helper import retrieve_jwks, decode_retreived_jwt
from src.user_helper import create_user


@app.route("/register", methods=['GET', 'POST'])
def register():
    # provide authentication page
    if request.method == 'GET':
        return render_template("register.html")

    if request.method == 'POST':

        # if we got plaintext user registration
        if "username" in request.get_data().decode('ascii'):
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            first_name = request.form['first_name']
            last_name = request.form['last_name']

            logging.info(f"Registration attempt:\n\tusername: {username}\n\temail: {email}\n\tpassword: <redacted>\n\tfirst_name: {first_name}\n\tlast_name: {last_name}")

            # verify that the username is unique
            if database.lookup_by_username(username):
                logging.error(f"Collision with username '{database.lookup_by_email(username)}'")
                return render_template("register.html", bad_registration="user_exists")

            # verify that the email is unique
            if database.lookup_by_email(email):
                logging.error(f"Collision with email '{database.lookup_by_email(email)}'")
                return render_template("register.html", bad_registration="user_exists")

            # create new records for the user
            create_user(database, username, email, password, first_name, last_name)

            # TODO send email activation
            
            return redirect("/login")

        # assume that the user was redirected by sso, register via JWT, just revalidate
        else:
            # retreive data and parse out the token
            query_string = request.get_data().decode('ascii')
            unverified_jwt = parse.parse_qs(query_string)['credential'][0]

            logging.info(f"SSO registration attempted with '{unverified_jwt}'")

            valid_jwt = decode_retreived_jwt(unverified_jwt, retrieve_jwks(), GOOGLE_CLIENT_ID)

            # if this conditional is true it means a valid JWT credential, signed by google was sent to the registration form with a coliding email, the site will never do this normally as the user should just be logged in and provided a session.
            if database.lookup_by_email(valid_jwt['email']):
                logging.error(f"Site is probably being attached, collision with email from SSO registration redirection '{database.lookup_by_email(valid_jwt['email'])}'")
                return redirect('/')

            # create new records for the user
            create_user(database, "sso", valid_jwt['email'], "sso", valid_jwt['given_name'], valid_jwt['family_name'])

            return render_template("login.html",
                                   host_port=HOST_AND_PORT,
                                   google_client_id=GOOGLE_CLIENT_ID,
                                   good_registration="success")