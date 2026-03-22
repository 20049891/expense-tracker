from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from database.db import get_db

user_bp = Blueprint('user', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or session['user']['role'] != 'USER':
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@user_bp.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user']['id']
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    # Get total income
    cursor.execute("SELECT income FROM User WHERE userID = %s", (user_id,))
    income = cursor.fetchone()['income'] or 0

    # Get total expenses
    cursor.execute("SELECT SUM(amount) as total FROM Expense WHERE userID = %s", (user_id,))
    total_expense = cursor.fetchone()['total'] or 0

    # Calculate balance
    balance = float(income) - float(total_expense)

    # Get category wise expenses for pie chart
    cursor.execute("""
        SELECT category, SUM(amount) as total 
        FROM Expense 
        WHERE userID = %s 
        GROUP BY category
    """, (user_id,))
    category_expenses = cursor.fetchall()
    
    # Categories for form
    cursor.execute("SELECT * FROM Category")
    categories = cursor.fetchall()

    cursor.close()
    
    return render_template('dashboard.html', 
                         balance=balance, 
                         income=income, 
                         total_expense=total_expense,
                         category_expenses=category_expenses,
                         categories=categories)

@user_bp.route('/transactions', methods=['GET', 'POST'])
@login_required
def transactions():
    user_id = session['user']['id']
    db = get_db()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        amount = request.form.get('amount')
        date = request.form.get('date')
        category = request.form.get('category')
        mode = request.form.get('mode')
        notes = request.form.get('notes', '').strip()

        try:
            if float(amount) < 0:
                flash('Expense amount cannot be negative.', 'error')
                return redirect(url_for('user.transactions'))
        except (ValueError, TypeError):
            flash('Invalid amount.', 'error')
            return redirect(url_for('user.transactions'))

        cursor.execute(
            "INSERT INTO Expense (userID, amount, date, category, mode, notes) VALUES (%s, %s, %s, %s, %s, %s)",
            (user_id, amount, date, category, mode, notes)
        )
        db.commit()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('user.transactions'))

    # GET request - fetch all transactions
    cursor.execute("SELECT * FROM Expense WHERE userID = %s ORDER BY date DESC", (user_id,))
    expenses = cursor.fetchall()

    cursor.execute("SELECT * FROM Category")
    categories = cursor.fetchall()

    cursor.close()
    return render_template('transactions.html', expenses=expenses, categories=categories)


@user_bp.route('/transaction/delete/<int:expense_id>', methods=['POST'])
@login_required
def delete_transaction(expense_id):
    user_id = session['user']['id']
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM Expense WHERE expenseID = %s AND userID = %s", (expense_id, user_id))
    db.commit()
    cursor.close()
    flash('Transaction deleted!', 'success')
    return redirect(url_for('user.transactions'))


@user_bp.route('/budgets', methods=['GET', 'POST'])
@login_required
def budgets():
    user_id = session['user']['id']
    db = get_db()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        category = request.form.get('category')
        limit = request.form.get('limitAmount')
        
        try:
            # Upsert budget limit
            cursor.execute("""
                INSERT INTO Budget (userID, category, limitAmount) 
                VALUES (%s, %s, %s) 
                ON DUPLICATE KEY UPDATE limitAmount = %s
            """, (user_id, category, limit, limit))
            db.commit()
            flash('Budget updated successfully!', 'success')
        except Exception as e:
            db.rollback()
            flash('Error saving budget.', 'error')

        return redirect(url_for('user.budgets'))

    # Get budgets and expenses to calculate progress
    cursor.execute("""
        SELECT b.category, b.limitAmount, IFNULL(SUM(e.amount), 0) as spent
        FROM Budget b
        LEFT JOIN Expense e ON b.userID = e.userID AND b.category = e.category AND MONTH(e.date) = MONTH(CURRENT_DATE()) AND YEAR(e.date) = YEAR(CURRENT_DATE())
        WHERE b.userID = %s
        GROUP BY b.category, b.limitAmount
    """, (user_id,))
    budget_data = cursor.fetchall()

    cursor.execute("SELECT * FROM Category")
    categories = cursor.fetchall()

    cursor.close()
    return render_template('budgets.html', budget_data=budget_data, categories=categories)
