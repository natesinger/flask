# Inheretance from main
from __main__ import (
    GOOGLE_DISCOVERY_URL
)

import requests
import logging
import json
import jwt

from urllib3.exceptions import NewConnectionError

def retrieve_jwks(disco:str=GOOGLE_DISCOVERY_URL) -> object:
    """
    Retrieves the valid jwks for Google OAuth2.
    disco:str - providers discovery document as a HTTP URI

    returns:object - valid public keys based on the discovery document
    """

    # Retrieve the discovery document
    try:
        discovery_document = requests.get(disco).json()
    except NewConnectionError:
        logging.error("Failed to retreive discovery document.")

    # Retrieve the keys
    try:
        jwks = requests.get(discovery_document['jwks_uri']).json()
    except NewConnectionError:
        logging.error("Failed to retreive jwks.")

    # Format the keys
    public_keys = {}
    try:
        for jwk in jwks['keys']:
            kid = jwk['kid']
            public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
    except Exception as e:
        logging.error(f"Something unexpected occured during key parsing: {e}")


    return public_keys


def decode_retreived_jwt(jwt_to_validate, public_keys, google_client_id):
    # Validate the signature of the key
    kid = jwt.get_unverified_header(jwt_to_validate)['kid']
    public_key = public_keys[kid]

    try:
        return (jwt.decode(jwt_to_validate,
                         key=public_key,
                         audience=google_client_id,
                         issuer = "https://accounts.google.com",
                         algorithms=['RS256']))
        
    except Exception as e:
        logging.error(f"Something unexpected occured during signature validation: {e}")
