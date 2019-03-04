from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import database

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'matrix'

app.secret_key = "any random string"

database.db = SQLAlchemy(app)

from models.member import Member
from models.event import Event
from models.financial import Financial
from models.product import Product
from models.team import Team
from models.training import Training

database.db.create_all()

from controllers.defaults import *
from controllers.member import *
from controllers.event import *
from controllers.financial import *
from controllers.product import *
from controllers.team import *
from controllers.training import *

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
