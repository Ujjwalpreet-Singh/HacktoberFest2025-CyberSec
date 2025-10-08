from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template
from models import Campaign,db
from services.email_service import send_phishing_email

campaigns_bp = Blueprint('campaigns', __name__)


@campaigns_bp.route('/campaigns', methods=['POST'])
def create_campaign():
    print("hello")
    data = request.json
    campaign = Campaign(
        name=data['name'],
        target_email=data['target_email'],
        subject=data['subject'],
        body=data['body']
    )
    db.session.add(campaign)
    db.session.commit()

    return jsonify({
        'message': 'Campaign created.',
        'campaign_id': campaign.id  # Return campaign_id to the frontend
    }), 201


@campaigns_bp.route('/send_email/<int:campaign_id>', methods=['POST'])
def send_email(campaign_id):
    data = request.json
    campaign = Campaign.query.get(campaign_id)

    if not campaign:
        return jsonify({'error': 'Campaign not found'}), 404

    # Update the body with the final version containing tracking links
    campaign.body = data['body']
    send_phishing_email(campaign.target_email, campaign.subject, campaign.body)

    campaign.sent = True
    db.session.commit()

    return jsonify({'message': 'Email sent with tracking links.','success':True}), 200


