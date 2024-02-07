import psycopg2

# Establish a connection to PostgeSQL database
conn = psycopg2.connect(
    dbname="portal_data_base",
    user="postgres",
    password="abc",
    host="",
    port="5432"
)

cursor = conn.cursor()

primary_key_value = '123-abc'

query = "SELECT * FROM parts WHERE part_id = %s;"

cursor.execute(query, (primary_key_value,))

row = cursor.fetchone()

print(row)

cursor.close()
conn.close()