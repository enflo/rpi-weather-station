import psycopg2

from src.settings import (
    POSTGRES_DBNAME,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_TABLE,
    POSTGRES_USER,
)


class SendDataPostgres:
    def __init__(self, data):
        self.data = data

    def send(self):
        """Send data to PostgreSQL database."""
        try:
            # Connect to the database
            connection = self._get_connection()
            
            # Create a cursor to execute SQL queries
            cursor = connection.cursor()
            
            # Insert data into the table
            self._insert_data(cursor)
            
            # Commit the transaction
            connection.commit()
            
            # Close the cursor and connection
            cursor.close()
            connection.close()
            
        except Exception as e:
            print(f"Failed to send data to PostgreSQL: {e}")

    def _get_connection(self):
        """Create and return a database connection."""
        return psycopg2.connect(
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            dbname=POSTGRES_DBNAME
        )
    
    def _insert_data(self, cursor):
        """Insert data into the database."""
        # Get column names and values from the data dictionary
        columns = list(self.data.keys())
        values = [self.data[column] for column in columns]
        
        # Build the SQL query
        placeholders = ', '.join(['%s'] * len(columns))
        columns_str = ', '.join(columns)
        
        # Execute the query
        query = f"INSERT INTO {POSTGRES_TABLE} ({columns_str}) VALUES ({placeholders})"
        cursor.execute(query, values)