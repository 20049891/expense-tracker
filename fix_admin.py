from werkzeug.security import generate_password_hash
import mysql.connector

# Create the new secure hash for 'admin'
new_hash = generate_password_hash('admin')

def fix_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            port=3306,
            database="smart_expense_tracker"
        )
        cursor = connection.cursor()
        cursor.execute("UPDATE User SET password = %s WHERE email = 'admin@tracker.com'", (new_hash,))
        connection.commit()
        print(f"Successfully updated Admin password. New Hash: {new_hash}")
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Failed to update db: {e}")

if __name__ == "__main__":
    fix_db()
