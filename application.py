from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_basicauth import BasicAuth
import os
import database

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'matrix'

app.secret_key = "any random string"

database.db = SQLAlchemy(app)
basic_auth = BasicAuth(app)

from models import *

database.db.create_all()

from controllers import *

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
