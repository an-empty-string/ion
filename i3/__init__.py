from flask import Flask
from database import db_session
app = Flask(__name__)
app.secret_key = "replace this with the real key"
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

import views

