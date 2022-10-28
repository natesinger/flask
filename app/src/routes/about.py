# Inheretance from main
from __main__ import (
    app
)

# Third-party libraries
from flask import (
    render_template
)

@app.route("/about")
def about(): 
    return render_template("about.html")