import os
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Configure the database - use SQLite for better compatibility
# SQLite is simpler to deploy and works on all platforms
database_path = os.environ.get("DATABASE_PATH", "app.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{database_path}"
print(f"Using database: {app.config['SQLALCHEMY_DATABASE_URI']}")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the app with the extension
db.init_app(app)

with app.app_context():
    # Import the models here to ensure tables are created
    from models import Application
    db.create_all()

# Import routes after the app is created
from routes import *
