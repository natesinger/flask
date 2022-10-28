import mysql.connector
import logging

class Database:
    def __init__(self, host, username, password, database_name):
        self.host = host
        self.username = username
        self.password = password
        self.database_name = database_name

        self.__connect__()

    def __connect__(self) -> None:
        self.connector = mysql.connector.connect(host = self.host,
                                                 user = self.username,
                                                 password = self.password,
                                                 database = self.database_name)
        
        if self.connector.is_connected():
            db_info = self.connector.get_server_info()
            
            logging.info(f"Connected to MySQL server, version '{db_info}'")

    def lookup_by_email(self, email_address:str) -> tuple:
        try:
            cursor = self.connector.cursor(prepared=True)

            query_email_lookup = """SELECT * FROM accounts WHERE email=%s"""
            data = (email_address,)

            cursor.execute(query_email_lookup, data)

            return cursor.fetchone()

        except Exception as e:
            print("Error while connecting to MySQL", e)
    
    def lookup_by_username(self, username:str) -> tuple:
        try:
            cursor = self.connector.cursor(prepared=True)

            query_username_lookup = """SELECT * FROM accounts WHERE username=%s"""
            data = (username,)

            cursor.execute(query_username_lookup, data)

            return cursor.fetchone()

        except Exception as e:
            print("Error while connecting to MySQL", e)

    def lookup_uid_by_session(self, session_token:str) -> tuple:
        try:
            cursor = self.connector.cursor(prepared=True)

            query_sessionid_lookup = """SELECT * FROM sessions WHERE session_id=%s;"""
            data = (session_token,)

            cursor.execute(query_sessionid_lookup, data)
            retreived_uid = cursor.fetchone()[1]

            return retreived_uid

        except Exception as e:
            print("Error while connecting to MySQL", e)
    
    def lookup_role_by_uid(self, user_id:str) -> str:
        try:
            cursor = self.connector.cursor(prepared=True)

            query_uid_lookup = """SELECT * FROM accounts WHERE user_id=%s;"""
            data = (user_id,)

            cursor.execute(query_uid_lookup, data)
            retreived_roles = cursor.fetchone()[7]

            return retreived_roles

        except Exception as e:
            print("Error while connecting to MySQL", e)

    def lookup_account_by_uid(self, user_id:str) -> str:
        try:
            cursor = self.connector.cursor(prepared=True)

            query_uid_lookup = """SELECT * FROM accounts WHERE user_id=%s;"""
            data = (user_id,)

            cursor.execute(query_uid_lookup, data)
            retreived_account = cursor.fetchone()

            return retreived_account

        except Exception as e:
            print("Error while connecting to MySQL", e)

    def create_account(self, user_id:str, username:str, password_hash:str,
                     given_name:str, family_name:str, email:str, 
                     email_verified:bool, roles:str) -> None:
        
        try:
            cursor = self.connector.cursor(prepared=True)

            query_account_create = """INSERT INTO accounts (
                    user_id,
                    username,
                    password_hash,
                    given_name,
                    family_name,
                    email,
                    email_verified,
                    roles
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
            data = (user_id,
                    username,
                    password_hash,
                    given_name,
                    family_name,
                    email,
                    email_verified,
                    roles)

            cursor.execute(query_account_create, data)
            cursor.close()
            
            self.connector.commit()

        except Exception as e:
            print("Error while inserting into MySQL", e)


    def create_session(self, session_id:str, user_id:str, expiration_epoch:int) -> None:
        try:
            cursor = self.connector.cursor(prepared=True)

            query_session_create = """INSERT INTO sessions (
                    session_id,
                    user_id,
                    expiration
                ) VALUES (%s,%s,%s)"""
            data = (session_id,
                    user_id,
                    expiration_epoch)

            cursor.execute(query_session_create, data)
            cursor.close()
            
            self.connector.commit()

        except Exception as e:
            print("Error while inserting into MySQL", e)

    def purge_session(self, session_token:str) -> None:
        try:
            cursor = self.connector.cursor(prepared=True)

            query_purge_session = """DELETE FROM sessions WHERE session_id=%s"""
            data = (session_token,)

            cursor.execute(query_purge_session, data)
            cursor.close()
            
            self.connector.commit()

        except Exception as e:
            print("Error while deleting from MySQL", e)