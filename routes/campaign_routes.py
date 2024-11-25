from flask import Blueprint, render_template, request, redirect, url_for
from models import Campaign
from app import db
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Define Blueprint
campaign_bp = Blueprint('campaign_bp', __name__)

@campaign_bp.route('/')
def home():
    return render_template('index.html')

@campaign_bp.route('/add_campaign', methods=['GET', 'POST'])
def add_campaign():
    if request.method == 'POST':
        name = request.form['name']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        engagement_rate = request.form['engagement_rate']
        reach = request.form['reach']
        conversion_rate = request.form['conversion_rate']
        client_id = request.form['client_id']

        campaign = Campaign(name=name, start_date=start_date, end_date=end_date,
                            engagement_rate=engagement_rate, reach=reach,
                            conversion_rate=conversion_rate, client_id=client_id)

        db.session.add(campaign)
        db.session.commit()

        return redirect(url_for('campaign_bp.home'))  # Redirect to homepage after success

    return render_template('campaign_form.html')

@campaign_bp.route('/visualize_campaign/<int:id>')
def visualize_campaign(id):
    campaign = Campaign.query.get(id)
    if campaign:
        metrics = ['Engagement Rate', 'Reach', 'Conversion Rate']
        values = [campaign.engagement_rate, campaign.reach, campaign.conversion_rate]
        
        fig, ax = plt.subplots()
        ax.bar(metrics, values)

        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)

        img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')

        return render_template('visualization.html', img_base64=img_base64, campaign=campaign)

    return "Campaign not found", 404
