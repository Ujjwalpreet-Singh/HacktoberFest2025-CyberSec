from flask import Blueprint, jsonify, Response, render_template, session, redirect, url_for,request
from models import Campaign,db
import csv
import io

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/create',methods=['GET'])
def create_page():
    if not session.get('logged_in'):
        return redirect((url_for('index')))

    template = request.args.get('template')

    if template == 'password-reset':
        return render_template('pass_reset.html')
    elif template == "document-share":
        return render_template('doc_share.html')
    elif template == "account-verification":
        return render_template("acc_verify.html")
    else:
        return render_template('create_campaign.html')


@admin_bp.route('/admin/campaigns', methods=['GET'])
def list_campaigns():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    campaigns = Campaign.query.all()
    data = [{
        'id': campaign.id,
        'name': campaign.name,
        'target_email': campaign.target_email,
        'subject': campaign.subject,
        'body': campaign.body,
        'sent': campaign.sent,
        'opened': campaign.opened,
        'clicked': campaign.clicked,
        'submitted': campaign.submitted,
        'username_submitted' : campaign.submitted_username,
        'password_submitted' : campaign.submitted_password
    } for campaign in campaigns]
    return jsonify(data)

@admin_bp.route('/admin/campaigns/view', methods=['GET'])
def campaigns_page():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    return render_template('campaigns.html')  # HTML file with JS fetch


@admin_bp.route('/dashboard', methods=['GET'])
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('index'))  # redirect to login if not authenticated

    campaigns = Campaign.query.all()
    return render_template('admin_dashboard.html', campaigns=campaigns)

@admin_bp.route('/admin/campaigns/<int:campaign_id>', methods=['GET'])
def get_campaign(campaign_id):
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    campaign = Campaign.query.get_or_404(campaign_id)
    return jsonify({
        'id': campaign.id,
        'name': campaign.name,
        'target_email': campaign.target_email,
        'subject': campaign.subject,
        'body': campaign.body,
        'sent': campaign.sent,
        'opened': campaign.opened,
        'clicked': campaign.clicked,
        'submitted': campaign.submitted,
        'username_submitted' : campaign.submitted_username,
        'password_submitted' : campaign.submitted_password
    })

@admin_bp.route('/admin/campaigns/view/<int:campaign_id>', methods=['GET'])
def single_campaigns_page(campaign_id):
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    return render_template('single_view.html', campaign_id=campaign_id)


@admin_bp.route('/admin/export', methods=['GET'])
def export_csv():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    campaigns = Campaign.query.all()
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(['ID', 'Name', 'Target Email', 'Subject', 'Sent', 'Opened', 'Clicked', 'Submitted'])
    for c in campaigns:
        writer.writerow([
            c.id, c.name, c.target_email, c.subject,
            c.sent, c.opened, c.clicked, c.submitted
        ])

    response = Response(output.getvalue(), mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=phishing_campaigns.csv'
    return response

@admin_bp.route('/admin/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@admin_bp.route('/admin/campaigns/clear',methods=['POST'])
def clear_campaigns():
    if not session.get('logged_in'):
        return redirect(url_for('index'))  # Forbidden

    try:
        num_deleted = db.session.query(Campaign).delete()
        db.session.commit()
        return jsonify({"status": "success", "message": f"{num_deleted} campaigns deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

