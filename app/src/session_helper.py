import logging
import os

def create_session(database:object, user_id:str) -> str:
    session_id = os.urandom(32)

    database.create_account(user_id,
                            username,
                            password_hash_salted,
                            first_name,
                            last_name,
                            email,
                            email_verified, 
                            roles)