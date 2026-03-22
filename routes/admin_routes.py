from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from functools import wraps
from database.db import get_db

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or session['user']['role'] != 'ADMIN':
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM User WHERE role = 'USER'")
    users = cursor.fetchall()
    
    # Quick stats
    cursor.execute("SELECT COUNT(*) as cnt FROM User WHERE role = 'USER'")
    total_users = cursor.fetchone()['cnt']
    
    cursor.close()
    return render_template('admin_dashboard.html', users=users, total_users=total_users)

@admin_bp.route('/user/status/<int:user_id>/<action>', methods=['POST'])
@admin_required
def update_user_status(user_id, action):
    status = 'ACTIVE' if action == 'activate' else 'BLOCKED'
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE User SET status = %s WHERE userID = %s AND role='USER'", (status, user_id))
    db.commit()
    cursor.close()
    flash(f"User status updated to {status}", 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/categories', methods=['GET', 'POST'])
@admin_required
def categories():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        icon = request.form.get('icon', '').strip()
        
        if not name:
            flash("Category name cannot be empty.", "error")
            return redirect(url_for('admin.categories'))
            
        cursor.execute("INSERT INTO Category (name, icon, is_default) VALUES (%s, %s, TRUE)", (name, icon))
        db.commit()
        flash("Category added!", "success")
        return redirect(url_for('admin.categories'))

    cursor.execute("SELECT * FROM Category")
    cats = cursor.fetchall()
    cursor.close()
    return render_template('admin_categories.html', categories=cats)

@admin_bp.route('/categories/delete/<int:cat_id>', methods=['POST'])
@admin_required
def delete_category(cat_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM Category WHERE categoryID = %s", (cat_id,))
    db.commit()
    cursor.close()
    flash("Category deleted!", "success")
    return redirect(url_for('admin.categories'))

@admin_bp.route('/ai-monitoring')
@admin_required
def ai_monitoring():
    # Placeholder for AI model stats
    return render_template('admin_ai.html')
