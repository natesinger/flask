# Inheretance from main
from __main__ import (
    app
)

# Third-party libraries
from flask import (
    redirect
)

@app.route("/")
def index(): return redirect("/login")