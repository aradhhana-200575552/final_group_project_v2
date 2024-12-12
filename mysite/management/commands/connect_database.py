import mysql.connector

# # Connect to the MySQL RDS instance
# connection = mysql.connector.connect(
#     host="airpolution.cnieousumop3.us-east-1.rds.amazonaws.com",  # Replace with your endpoint
#     user="mydb",                            # Replace with your username
#     password="Aru331995"                # Replace with your password
# )

from django.core.management.base import BaseCommand
import mysql.connector

class Command(BaseCommand):
    help = 'Connect to the database and perform actions'

    def handle(self, *args, **kwargs):
        # Replace with your connection details
        connection = mysql.connector.connect(
            host="35.184.207.245",       # Public IP from Cloud SQL
            user="myself",       
            password="Aru331995",    
            database="firstdb",          
            port=3306                    
        )
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES;")
        for table in cursor.fetchall():
            print(table)

        connection.close()
        print("Database connection successful!")
