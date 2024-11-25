from .campaign_routes import campaign_bp

def register_routes(app):
    app.register_blueprint(campaign_bp)
