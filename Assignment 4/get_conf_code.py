import sqlite3

conn = sqlite3.connect("digibooth.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM users")
users = cursor.fetchall()
print("Users:", users)

# cursor.execute("DELETE FROM users")
# conn.commit()

# cursor.execute("SELECT * FROM users")
# print(cursor.fetchall())

conn.close()
exit()