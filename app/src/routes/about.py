# Inheretance from main
from __main__ import (
    app,
    database
)

# Third-party libraries
from flask import (
    render_template,
    request
)

# Internal imports
from src.authorization_helper import require_role


@app.route("/about")
def about():
    name = None

    if "Authorization" in request.cookies:
        # Ensure the token was extracted
        authorization_token = request.cookies['Authorization'].split(' ')[1]

        # Ensure a uid was retreived from the session
        retreived_uid = database.lookup_uid_by_session(authorization_token)
        retreived_account = database.lookup_account_by_uid(retreived_uid)

        if retreived_account: name=retreived_account[3]

    if name: return render_template("site/about.html", user=name)
    else: return render_template("site/about.html")