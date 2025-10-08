from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from routes.campaigns import campaigns_bp
from routes.tracking import tracking_bp
from routes.admin import admin_bp
from models import db

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = 'your_secret_key'  # Add a secret key for session security
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # or a full Postgres/MySQL URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
print("hello")
# Register blueprints
app.register_blueprint(campaigns_bp)
app.register_blueprint(tracking_bp)
app.register_blueprint(admin_bp)

# Create tables on first run
with app.app_context():
    db.create_all()

# Admin Login route (GET shows the login page, POST processes login)
@app.route('/', methods=['GET'])
def default():
    session['logged_in'] = False
    return redirect(url_for('index'))

@app.route('/admin',methods = ['GET','POST'])
def index():
    print("requesting...")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the credentials are correct
        if username == 'admin' and password == 'admin123':
            print("logged in")# Replace with secure checks
            session['logged_in'] = True # Set session variable to indicate login success
            return redirect(url_for('admin.dashboard'))  # Redirect to admin dashboard

        return 'Invalid credentials', 401  # Display error if login fails

    return render_template('admin_login.html')  # Display the login form

if __name__ == '__main__':
    app.run(debug=True)
