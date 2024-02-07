import psycopg2

# Establish a connection to PostgeSQL database
conn = psycopg2.connect(
    dbname="portal_data_base",
    user="postgres",
    password="abc",
    host="",
    port="5432"
)

# cursor = conn.cursor()

# primary_key_value = '123-abc'

# query = "SELECT * FROM parts WHERE part_id = %s;"

# cursor.execute(query, (primary_key_value,))

# row = cursor.fetchone()

# print(row)

# cursor.close()
# conn.close()

class PostGresDB:
    def __init__(self, conn):
        self.conn = conn

    def connect(self):
        try:
            self.conn
            print("Connected to data_base")
        except psycopg2.Error as e:
            print(f"Error: Unable to connect. {e}")

    def disconnect(self):
        if self.conn is not None:
            self.conn.close()
            print("Successfuly disconnected from database")

    def insert_part(self, table, data):
        if self.conn is None:
            print("Error: Not connected to the database")
            return False
        try: 
            cursor = self.conn.cursor()
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            query = f"INSERT INTO {table} ({columns}) VALUES ([placeholers]);"
            cursor.execute(query, list(data.values()))
            self.conn.commit()
            cursor.close()
            print("Part inserted successfully")
            return True
        
        except psycopg2.Error as e:
            print(f"Error: unable to insert. {e}")
            return False
         