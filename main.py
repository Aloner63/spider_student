import mysql.connector
import os

# Establish connection
conn = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='root',
    database='spider'
)

cursor = conn.cursor()



