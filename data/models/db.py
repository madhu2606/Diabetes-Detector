import sqlite3

conn = sqlite3.connect('database.db')
print("Opened database successfully")

# conn.execute('CREATE TABLE users (fullname TEXT, email TEXT, username TEXT, password TEXT,mobile INTEGER)')
conn.execute('CREATE TABLE predictions (ID INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT, gender TEXT, Age INTEGER, Pregnancies INTEGER,Glucose INTEGER,BloodPressure INTEGER,SkinThickness INTEGER,Insulin INTEGER,BMI INTEGER,HeartRateVariability INTEGER, mobile INTEGER)')
print ("Table created successfully")
conn.close()


# cursor = conn.cursor()
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# print(cursor.fetchall())