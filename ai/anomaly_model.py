import pandas as pd
from sklearn.ensemble import IsolationForest
import warnings
warnings.filterwarnings('ignore')

def detect_anomalies(df):
    """
    Detects unusual transactions (anomalies) using Isolation Forest.
    Returns a list of alerts for the user.
    """
    if df.empty or len(df) < 10:
        return []

    X = df[['amount']]
    median_spend = df['amount'].median()
    
    # contamination defines the proportion of outliers in the data set
    model = IsolationForest(contamination='auto', random_state=42)
    df['anomaly'] = model.fit_predict(X)
    
    # Fallback to flag massive singular spikes that Forest might miss on small datasets
    # using Median is crucial to prevent the spike from inflating the base metric
    df.loc[df['amount'] > (median_spend * 5), 'anomaly'] = -1
    
    # Anomaly values are -1. Normal are 1.
    anomalies_df = df[df['anomaly'] == -1]
    
    alerts = []
    for _, row in anomalies_df.iterrows():
        alerts.append({
            "message": f"Unusual spending detected! You spent ₹{row['amount']:,.2f} on {row['category']} on {row['date'].strftime('%Y-%m-%d')}.",
            "amount": row['amount'],
            "category": row['category'],
            "date": row['date']
        })
        
    return alerts
