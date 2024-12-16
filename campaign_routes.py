# import matplotlib
# matplotlib.use('Agg')  # Use non-GUI backend
# import matplotlib.pyplot as plt

from flask import Blueprint, render_template, request, redirect, url_for
from models import Campaign
from db import db  # Ensure db is correctly imported from the db.py module
from datetime import datetime  # Import datetime module

from io import BytesIO
import base64
import plotly.graph_objects as go

# Define Blueprint
campaign_bp = Blueprint('campaign_bp', __name__)

@campaign_bp.route('/')
def home():
    campaigns = Campaign.query.all()  # Fetch all campaigns from the database
    return render_template('index.html', campaigns=campaigns)

@campaign_bp.route('/add', methods=['GET', 'POST'])  # Handle both GET and POST for adding campaigns
def add_campaign():
    if request.method == 'POST':
        try:
            # Retrieve form data
            name = request.form['name']
            start_date_str = request.form['start_date']
            end_date_str = request.form['end_date']
            engagement_rate = float(request.form['engagement_rate'])  # Convert to float
            reach = int(request.form['reach'])  # Convert to int
            conversion_rate = float(request.form['conversion_rate'])  # Convert to float
            client_id = int(request.form['client_id'])  # Convert to int

            # Try parsing date in different formats
            date_formats = ['%Y-%m-%d', '%m/%d/%Y']
            start_date, end_date = None, None

            # Parse start_date
            for date_format in date_formats:
                try:
                    start_date = datetime.strptime(start_date_str, date_format).date()
                    break
                except ValueError:
                    continue

            if not start_date:
                return f"Invalid date format for start date. Please use either YYYY-MM-DD or MM/DD/YYYY.", 400

            # Parse end_date
            for date_format in date_formats:
                try:
                    end_date = datetime.strptime(end_date_str, date_format).date()
                    break
                except ValueError:
                    continue

            if not end_date:
                return f"Invalid date format for end date. Please use either YYYY-MM-DD or MM/DD/YYYY.", 400

            # Create and save the campaign
            campaign = Campaign(
                name=name,
                start_date=start_date,
                end_date=end_date,
                engagement_rate=engagement_rate,
                reach=reach,
                conversion_rate=conversion_rate,
                client_id=client_id,
            )
            db.session.add(campaign)
            db.session.commit()

            return redirect(url_for('campaign_bp.home'))  # Redirect to home page after adding the campaign

        except KeyError as e:
            # Handle missing form fields (e.g., 'client_id') or incorrect data
            return f"Missing form data: {str(e)}", 400
        except ValueError as e:
            # Handle incorrect data types (e.g., trying to convert a non-numeric value)
            return f"Invalid input: {str(e)}", 400

    return render_template('campaign_form.html')  # Render the campaign form for GET requests


@campaign_bp.route('/visualize/<int:id>')
def visualize_campaign(id):
    campaign = Campaign.query.get(id)
    if not campaign:
        return "Campaign not found", 404

    # Prepare data for visualization
    metrics = ['Engagement Rate', 'Reach', 'Conversion Rate']
    values = [campaign.engagement_rate, campaign.reach, campaign.conversion_rate]

    # Create the bar chart using Plotly
    fig = go.Figure([go.Bar(x=metrics, y=values, marker_color=['skyblue', 'lightgreen', 'lightcoral'])])
    fig.update_layout(
        title=f"Campaign: {campaign.name} - Performance Overview",
        xaxis_title="Metrics",
        yaxis_title="Values"
    )

    # Return the Plotly figure as HTML
    return fig.to_html()

@campaign_bp.route('/delete/<int:id>', methods=['POST'])
def delete_campaign(id):
    """Delete a campaign by ID."""
    campaign = Campaign.query.get(id)
    if campaign:
        db.session.delete(campaign)
        db.session.commit()
        return redirect(url_for('campaign_bp.home'))
    return "Campaign not found", 404

@campaign_bp.route('/update/<int:id>', methods=['GET', 'POST'])
def update_campaign(id):
    """Update details of an existing campaign."""
    campaign = Campaign.query.get(id)
    if not campaign:
        return "Campaign not found", 404

    if request.method == 'POST':
        try:
            # Update campaign details
            campaign.name = request.form['name']
            campaign.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
            campaign.end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
            campaign.engagement_rate = float(request.form['engagement_rate'])
            campaign.reach = int(request.form['reach'])
            campaign.conversion_rate = float(request.form['conversion_rate'])
            campaign.client_id = int(request.form['client_id'])

            db.session.commit()
            return redirect(url_for('campaign_bp.home'))

        except ValueError as e:
            return f"Invalid input: {str(e)}", 400

    return render_template('campaign_form.html', campaign=campaign)