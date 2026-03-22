import mysql.connector
import os

def setup_database():
    print("Setting up database...")
    try:
        # Connect to MySQL Server (make sure XAMPP is running)
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            port=3306 
            # no database specified initially so we can create it
        )
        
        cursor = connection.cursor()
        
        # Read the schema SQL file
        schema_path = os.path.join(os.path.dirname(__file__), 'database', 'schema.sql')
        with open(schema_path, 'r', encoding='utf-8') as file:
            sql_script = file.read()
            
        # Execute the SQL statements
        # We split by semicolon to execute them one by one
        for statement in sql_script.split(';'):
            if statement.strip():
                cursor.execute(statement)
                
        connection.commit()
        print("Database 'smart_expense_tracker' and tables created successfully!")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    setup_database()
