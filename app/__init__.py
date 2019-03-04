# Importa os padrões e operadores do FLask
from flask import Flask

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Import a module / component using its blueprint handler variable (mod_auth)
from app.controllers.defaults import *
from app.controllers.member import *
from app.controllers.event import *
from app.controllers.financial import *
from app.controllers.product import *
from app.controllers.team import *
from app.controllers.training import *

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()