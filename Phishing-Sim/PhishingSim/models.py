from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    target_email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(150), nullable=False)
    body = db.Column(db.Text, nullable=False)
    sent = db.Column(db.Boolean, default=False)
    opened = db.Column(db.Boolean, default=False)
    clicked = db.Column(db.Boolean, default=False)
    submitted = db.Column(db.Boolean, default=False)

    submitted_username = db.Column(db.String(120))
    submitted_password = db.Column(db.String(120))

