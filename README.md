# Smart Expense Tracker with AI Insights
**Academic Submission / Final Year Project**

The Smart Expense Tracker is an intelligent financial management web application built using Flask, MySQL, Bootstrap, and Scikit-learn. It acts as a personal financial advisor, allowing users to track expenses and receive data-driven AI insights.

## Technologies Used
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5, Chart.js
- **Backend**: Python, Flask
- **Database**: MySQL (XAMPP compatibility)
- **AI / ML**: Scikit-Learn, Pandas, NumPy
- **Models Used**:
  - Linear Regression (Expense Prediction)
  - K-Means Clustering (Spending Pattern categorization)
  - Isolation Forest (Anomaly/Unusual expense detection)

## Project Structure
```text
expense-tracker/
│
├── app.py                      # Main entrypoint and Flask server setup
├── requirements.txt            # Python dependencies
├── setup_db.py                 # Script to auto-initialize the MySQL database
│
├── database/                   
│   ├── db.py                   # MySQL connection setup for Flask context
│   └── schema.sql              # Database Tables Scheme
│
├── routes/                     
│   ├── auth_routes.py          # Registration & Login logic
│   ├── user_routes.py          # User Dashboard, CRUD Operations, Budgets
│   ├── ai_routes.py            # Bridge between UI and Scikit-learn
│   └── admin_routes.py         # Admin User & Category panels
│
├── ai/                         
│   ├── anomaly_model.py        # Isolation Forest logic
│   ├── pattern_model.py        # K-Means clustering logic
│   └── prediction_model.py     # Linear Regression predictions
│
├── reports/
│   └── pdf_generator.py        # Excel report builder logic
│
└── frontend/
    ├── static/
    │   ├── css/style.css       # Custom aesthetics
    │   └── js/main.js          # Theme toggler & basic interaction
    └── templates/              # HTML files (base.html, dashboard, etc.)
```

## Setup & Deployment Guide

1. **Pre-requisites**:
   - Install XAMPP (or any MySQL server). Start the MySQL service on port 3306.
   - Install Python 3.9+ 

2. **Installation Steps**:
   ```bash
   # Create virtual environment (optional but recommended)
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Setup the Database (Ensure MySQL is running without password for root, or edit database/db.py & setup_db.py)
   python setup_db.py
   
   # Run the server
   python app.py
   ```

3. **Access the App**:
   - Open browser at `http://localhost:5000`
   - **Default Admin User**:
     - Email: `admin@tracker.com`
     - Password: `admin`
     *(This is auto-populated by the schema)*

## Testing Strategy
- **Authentication**: Try to access `/user/dashboard` without logging in. You should be redirected.
- **Transactions**: Add combinations of positive and negative data to test boundary conditions.
- **AI Integration**: Add at least 10 varied transactions (cheap ones like Food 100rs, and unusually high ones like Shopping 15000rs) to trigger the *Isolation Forest* detection in the AI tab. Add transactions scaling up over multiple days to see the *Linear Regression* prediction adjust.
- **Budgets**: Set a budget for 'Food' at 2000rs. Add generic 'Food' expenses and watch the progress bar change from Green -> Yellow -> Red.

*Developed by AI Engineer, as requested.*
