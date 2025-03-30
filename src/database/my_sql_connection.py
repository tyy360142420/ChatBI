import mysql.connector

mysql_conn = mysql.connector.connect(
    host="127.0.0.1",
    user="tyy",
    password="TangYiYe@123",
    database="spider"
)

cursor = mysql_conn.cursor()
cursor.execute("select * from table1")
result = cursor.fetchall()
for row in result:
    print(row)


mysql_conn.close()