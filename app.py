from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///campaigns.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'your_secret_key_here'  # Secret key for session management

    # Initialize the db
    db.init_app(app)

    # Register the routes using the function from the routes module
    from routes import register_routes
    register_routes(app)

    # Create tables if they don't exist
    with app.app_context():
        db.create_all()  # Creates all tables

    return app
