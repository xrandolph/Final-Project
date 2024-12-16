from flask import Flask
from db import db  # Import db from db.py
from campaign_routes import campaign_bp

def create_app():
    app = Flask(__name__)

    # Configure database and other settings
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///campaigns.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'your_secret_key_here'

    # Initialize the db
    db.init_app(app)

    # Register the blueprint with the appropriate prefix
    app.register_blueprint(campaign_bp, url_prefix='/campaigns')

    # Create tables if they don't exist
    with app.app_context():
        db.create_all()

    return app