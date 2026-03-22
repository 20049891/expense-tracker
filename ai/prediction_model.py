import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import warnings
warnings.filterwarnings('ignore')

def predict_next_month_expenses(df):
    """
    Uses Linear Regression to predict the next month's total expense 
    based on historical daily spending.
    """
    if df.empty or len(df) < 5:
        # Not enough data for a meaningful prediction
        return {"amount": None, "message": "More transaction data needed to predict next month's expenses."}

    # Group by date to get daily totals
    df['date'] = pd.to_datetime(df['date'])
    daily_expenses = df.groupby('date')['amount'].sum().reset_index()
    daily_expenses = daily_expenses.sort_values('date')

    # Convert dates to ordinal values for regression
    daily_expenses['date_ordinal'] = daily_expenses['date'].map(pd.Timestamp.toordinal)
    
    # Remove extreme outliers (spikes > 5x avg) to prevent prediction blowup
    median_amount = daily_expenses['amount'].median()
    normal_transactions = daily_expenses[daily_expenses['amount'] <= (median_amount * 5)]
    
    if len(normal_transactions) >= 3:
        X_train = normal_transactions[['date_ordinal']]
        y_train = normal_transactions['amount']
    else:
        # Fallback if cleaning removed too much
        X_train = daily_expenses[['date_ordinal']]
        y_train = daily_expenses['amount']

    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predict for the next 30 days
    last_date = daily_expenses['date'].max()
    future_dates = [last_date + pd.Timedelta(days=i) for i in range(1, 31)]
    future_ordinals = np.array([d.toordinal() for d in future_dates]).reshape(-1, 1)

    predicted_daily_amounts = model.predict(future_ordinals)
    
    # Ensure no negative predictions
    predicted_daily_amounts = np.maximum(predicted_daily_amounts, 0)
    
    total_next_month_prediction = np.sum(predicted_daily_amounts)

    # Add 15% growth mention directly based on user requirement insight format
    # "Aapka agle mahine ka kharcha 15% badh sakta hai."
    current_month_total = df[df['date'].dt.month == last_date.month]['amount'].sum()
    
    if current_month_total > 0:
        percent_change = ((total_next_month_prediction - current_month_total) / current_month_total) * 100
    else:
        percent_change = 0

    message = f"Based on your trends, you are predicted to spend around ₹{total_next_month_prediction:,.2f} next month."
    
    if percent_change > 10:
        message += f" Caution: Aapka agle mahine ka kharcha {percent_change:.0f}% tak badh sakta hai."
    elif percent_change < -10:
        message += f" Great job! You are on track to reduce your expenses by {abs(percent_change):.0f}%."

    return {
        "amount": round(total_next_month_prediction, 2),
        "message": message,
        "percent_change": round(percent_change, 2)
    }
