'''
-*- coding: utf-8 -*-    
@File  : mysql_img_save.py
@author: zh
@NOTE  : mysql多image保存（基于路径）
@Time  : 2023/09/27 23:02
'''


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

# Sample image path
image_path = 'e:/images_2'

files = os.listdir(image_path)

try:
    for file in files:
        # Insert each file name into the database
        sql_insert_query = "INSERT INTO images (img_name,img_path) VALUES (%s,%s)"
        cursor.execute(sql_insert_query, (file,os.path.join(file,image_path)))
        conn.commit()
        print(f"File '{file}' inserted successfully.")

except mysql.connector.Error as error:
    print(f"Error: {error}")

finally:
    # Close the cursor and connection
    cursor.close()
    conn.close()
