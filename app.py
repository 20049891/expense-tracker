from flask import Flask, render_template, session, redirect, url_for, g
import os
from database.db import close_db

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')
app.secret_key = os.environ.get('SECRET_KEY', 'my_dev_secret_key')

# Close db connection after each request
app.teardown_appcontext(close_db)

# Import Routes
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.admin_routes import admin_bp
from routes.ai_routes import ai_bp
from reports.pdf_generator import reports_bp

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(ai_bp, url_prefix='/ai')
app.register_blueprint(reports_bp, url_prefix='/user/reports')

# Global context processor to inject user session info
@app.context_processor
def inject_user():
    return dict(user_session=session.get('user'))

@app.route('/')
def index():
    if 'user' in session:
        if session['user']['role'] == 'ADMIN':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('user.dashboard'))
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
