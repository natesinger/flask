import bcrypt
import uuid
import logging

def create_user(database:object,
                username:str,
                email:str,
                password:str,
                first_name:str,
                last_name:str) -> None:

    user_id = str(uuid.uuid1())
    password_hash_salted = generate_password_bcrypt(password)
    email_verified = False
    roles = "member"

    database.create_account(user_id,
                            username,
                            password_hash_salted,
                            first_name,
                            last_name,
                            email,
                            email_verified, 
                            roles)


def generate_password_bcrypt(password:str, rounds:int=10) -> str:
    # if this was requested by sso, ensure blank to prevent user/pass login,
    #   user can still reset password in the future if they want
    if password == "sso": return ""

    salt = bcrypt.gensalt(rounds=rounds)
    return bcrypt.hashpw(password.encode('ascii'), salt)


def validate_password_bcrypt(attempted_password:str, valid_password:str) -> bool:
    logging.info(f"Validating provided password '{attempted_password}' against '{valid_password}'")
    return bcrypt.checkpw(attempted_password.encode('ascii'), valid_password.encode('ascii'))

    
