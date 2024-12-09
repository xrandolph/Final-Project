from db import db  # Import db from db.py
from datetime import datetime

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    engagement_rate = db.Column(db.Float, nullable=False)
    reach = db.Column(db.Integer, nullable=False)
    conversion_rate = db.Column(db.Float, nullable=False)
    client_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Campaign {self.name}>"
