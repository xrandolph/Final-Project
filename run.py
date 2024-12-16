from app import create_app
from flask import redirect, url_for

app = create_app()

# Add a route for root to redirect to /campaigns/
@app.route('/')
def redirect_to_campaigns():
    return redirect(url_for('campaign_bp.home'))  # Redirect to the home page in the campaign blueprint

if __name__ == '__main__':
    app.run(debug=True)