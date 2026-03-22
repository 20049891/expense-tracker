import pandas as pd
from flask import send_file, Blueprint, request, session, redirect, url_for, render_template
import os
from io import BytesIO
from database.db import get_db

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/', methods=['GET', 'POST'])
def reports_page():
    if 'user' not in session or session['user']['role'] != 'USER':
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        # Delegate down to download
        return generate_excel_report()
        
    return render_template('reports.html')

@reports_bp.route('/download', methods=['POST'])
def generate_excel_report():
    if 'user' not in session or session['user']['role'] != 'USER':
        return redirect(url_for('auth.login'))
        
    user_id = session['user']['id']
    db = get_db()
    query = "SELECT amount, date, category, mode, notes FROM Expense WHERE userID = %s ORDER BY date DESC"
    df = pd.read_sql(query, db, params=(user_id,))
    
    if df.empty:
        return "No data to export", 400
        
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Expenses', index=False)
    
    output.seek(0)
    
    return send_file(output, download_name="expense_report.xlsx", as_attachment=True)
