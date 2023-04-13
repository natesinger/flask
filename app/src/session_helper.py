# Inheretance from main
from __main__ import (
    database,
    SESSION_TIMEOUT_SECONDS
)

import logging
import time
import secrets

def create_session(user_id:str) -> str:
    session_id = secrets.token_urlsafe(30)
    expiration = int(time.time() + SESSION_TIMEOUT_SECONDS)

    database.create_session(session_id=session_id, user_id=user_id, expiration_epoch=expiration)

    return session_id

def purge_session(session_token:str) -> None:
    database.purge_session(session_token)
    