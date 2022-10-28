# Python standard libraries
import os

# Third-party libraries
from flask import (
    Flask,
    redirect
)

# Internal imports
from src.database_interface import Database


# Environment
HOST_AND_PORT = os.environ.get("HOST_AND_PORT", None)
SESSION_TIMEOUT_SECONDS = os.environ.get("SESSION_TIMEOUT", None) or 604800 # 1 week

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

MYSQL_HOST = os.environ.get("MYSQL_HOST", None)
MYSQL_USER = os.environ.get("MYSQL_USER", None)
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", None)
MYSQL_DB = os.environ.get("MYSQL_DB", None)


database = Database(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)


app = Flask(__name__, template_folder="pages", static_folder="public", static_url_path="/public")
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)


# Routes
import src.routes.index
import src.routes.about
import src.routes.login
import src.routes.logout
import src.routes.register

# start application
if __name__ == "__main__": app.run(ssl_context="adhoc", debug=True)