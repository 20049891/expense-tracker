from flask import Blueprint, render_template, session, redirect, url_for, jsonify
from functools import wraps
from database.db import get_db
import pandas as pd
from ai.prediction_model import predict_next_month_expenses
from ai.pattern_model import get_spending_insights
from ai.anomaly_model import detect_anomalies

ai_bp = Blueprint('ai', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or session['user']['role'] != 'USER':
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@ai_bp.route('/insights')
@login_required
def insights():
    user_id = session['user']['id']
    db = get_db()
    
    # 1. Fetch Expenses Data
    query = "SELECT amount, date, category FROM Expense WHERE userID = %s ORDER BY date ASC"
    df = pd.read_sql(query, db, params=(user_id,))
    
    if df.empty:
         return render_template('insights.html', prediction=None, alerts=[], insights=[], empty=True)
    
    # Call ML Models
    prediction = predict_next_month_expenses(df.copy())
    cluster_insights = get_spending_insights(df.copy())
    anomalies = detect_anomalies(df.copy())
    
    return render_template('insights.html', 
                         prediction=prediction, 
                         alerts=anomalies, 
                         insights=cluster_insights,
                         empty=False)
