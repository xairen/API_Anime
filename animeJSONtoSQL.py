import pandas as pd
import mysql.connector

df = pd.read_csv('animedataset.csv')

# Connect to the MySQL database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password',
    database='animeDB'
)
cursor = conn.cursor()

insert_sql = """
INSERT INTO Anime (name, genre, size, rating) 
VALUES (%s, %s, %s, %s)
"""

for _, row in df.iterrows():
    record = (row['name'], row['genre'], row['size'], row.get('rating', None))
    cursor.execute(insert_sql, record)

conn.commit()
cursor.close()
conn.close()
