from app import db

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.String(20), nullable=False)
    end_date = db.Column(db.String(20), nullable=False)
    engagement_rate = db.Column(db.Float, nullable=False)
    reach = db.Column(db.Integer, nullable=False)
    conversion_rate = db.Column(db.Float, nullable=False)
    
    # Relationship with Client (one-to-many)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    client = db.relationship('Client', back_populates='campaigns')

    def __repr__(self):
        return f'<Campaign {self.name}>'

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_info = db.Column(db.String(200), nullable=False)

    # Relationship with Campaign
    campaigns = db.relationship('Campaign', back_populates='client')

    def __repr__(self):
        return f'<Client {self.name}>'
