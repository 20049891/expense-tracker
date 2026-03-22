import pandas as pd
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

def get_spending_insights(df):
    """
    Uses K-Means clustering to group spending patterns and 
    identify high-spending categories.
    """
    if df.empty or len(df) < 5:
        return ["Add more transactions to unlock category insights."]

    # Group by category
    category_totals = df.groupby('category')['amount'].sum().reset_index()
    
    # If we have very few categories, clustering isn't very useful
    if len(category_totals) < 3:
        high_cat = category_totals.loc[category_totals['amount'].idxmax()]
        return [f"Aapne is hafte {high_cat['category']} par zyada kharch kiya (₹{high_cat['amount']})."]

    # We cluster the categories based on their total amounts
    X = category_totals[['amount']]
    
    # Try 3 clusters: High, Medium, Low spending
    # If not enough categories, use 2
    n_clusters = min(3, len(category_totals))
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    category_totals['cluster'] = kmeans.fit_predict(X)
    
    # Identify which cluster represents "High Spending"
    cluster_centers = kmeans.cluster_centers_.flatten()
    high_spend_cluster = cluster_centers.argmax()
    
    high_spend_categories = category_totals[category_totals['cluster'] == high_spend_cluster]
    
    insights = []
    for _, row in high_spend_categories.iterrows():
        # Using the exact phrasing requested
        insights.append(f"Aapne is hafte {row['category']} par zyada kharch kiya (₹{row['amount']:,.2f}).")
        
    return insights
