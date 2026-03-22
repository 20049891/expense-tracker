from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM User WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user['password'], password):
            if user['status'] == 'BLOCKED':
                flash('Your account has been blocked by the admin.', 'error')
                return redirect(url_for('auth.login'))
            
            session['user'] = {
                'id': user['userID'],
                'name': user['name'],
                'email': user['email'],
                'role': user['role']
            }
            if user['role'] == 'ADMIN':
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('user.dashboard'))
        else:
            flash('Invalid email or password', 'error')

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        income = request.form.get('income', 0.0)

        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        # Check if email exists
        cursor.execute("SELECT * FROM User WHERE email = %s", (email,))
        if cursor.fetchone():
            flash('Email already registered', 'error')
            cursor.close()
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(password)
        try:
            cursor.execute(
                "INSERT INTO User (name, email, password, income, role) VALUES (%s, %s, %s, %s, 'USER')",
                (name, email, hashed_password, income)
            )
            db.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.rollback()
            flash('An error occurred during registration.', 'error')
        finally:
            cursor.close()

    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('auth.login'))
